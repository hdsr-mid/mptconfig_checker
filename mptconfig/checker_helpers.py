from mptconfig import constants
from mptconfig.fews_utilities import FewsConfig
from mptconfig.idmapping_choices import IntLocChoices
from mptconfig.utils import equal_dataframes
from pathlib import Path
from typing import Dict
from typing import List
from typing import TypeVar

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


PandasDFGroupBy = TypeVar(name="pd.core.groupby.generic.DataFrameGroupBy")  # noqa


class NewValidationCsv:
    def __init__(self, orig_filepath: Path, df: pd.DataFrame):
        self.orig_filepath = orig_filepath
        self.df = df
        self.validate_constructor()

    def validate_constructor(self):
        assert isinstance(self.orig_filepath, Path)
        assert self.orig_filepath.is_file()
        assert isinstance(self.df, pd.DataFrame)
        orig_df = pd.read_csv(
            filepath_or_buffer=self.orig_filepath,
            sep=None,
            engine="python",
        )
        assert not self.df.empty
        assert not equal_dataframes(expected_df=self.df, test_df=orig_df)


class NewValidationCsvCreator:
    def __init__(
        self,
        fews_config: FewsConfig,
        hoofdloc: constants.HoofdLocationSet,
        subloc: constants.SubLocationSet,
        waterstandloc: constants.WaterstandLocationSet,
        idmap_df: pd.DataFrame,
    ):
        self.fews_config = fews_config
        self.hoofdloc = hoofdloc
        self.subloc = subloc
        self.waterstandloc = waterstandloc
        self.idmap_df = idmap_df
        assert "is_in_a_validation" in self.idmap_df.columns
        self.ensure_config_matches_constants()

    def ensure_config_matches_constants(self) -> None:
        """Ensure that config has same validation csv names as define in constants. """
        config_validation_csv_filenames = [x for x in self.fews_config.MapLayerFiles.keys() if "validatie" in x]
        expected_validation_csv_filenames = [x.value for x in constants.ValidationCsvChoices]
        too_few = set(expected_validation_csv_filenames).difference(set(config_validation_csv_filenames))
        assert not too_few, f"too few validation csvs found in config {too_few}"

    def __get_int_loc_row_from_hoofd_sub_ow_loc_set(self, int_loc: str) -> pd.Series:
        row = None
        for loc_set_df in (self.hoofdloc.geo_df, self.subloc.geo_df, self.waterstandloc.geo_df):
            int_loc_df = loc_set_df[loc_set_df["LOC_ID"] == int_loc]
            if int_loc_df.empty:
                continue
            if row:
                logger.error(f"we expected only 1 row for int_loc {int_loc} in all mpt csvs. Returnng last found")
            row = int_loc_df
        return row

    def get_new_csv_data(self) -> pd.DataFrame:
        """Gather new validation csv data: filename, int_loc, startdate, enddate for location sets. """
        self.idmap_df["added_to_new_validation"] = False
        row_collector = []
        for idx, row in self.idmap_df.iterrows():
            if row["is_in_a_validation"]:
                continue
            row_int_loc = row["internalLocation"]
            row_int_par = row["internalParameter"]
            loc_set_row = self.__get_int_loc_row_from_hoofd_sub_ow_loc_set(int_loc=row_int_loc)
            if loc_set_row:
                self.idmap_df["is_in_a_mpt_csv"][idx] = True
                loc_type = row["TYPE"]
            else:
                if not IntLocChoices.is_ow(row_int_loc):
                    logger.debug(f"no validation csv for int_loc={row_int_loc}, int_par={row_int_par}")
                    continue
                loc_type = "waterstand"
            filename = constants.ValidationCsvChoices.get_validation_csv_name(int_par=row_int_par, loc_type=loc_type)
            if not filename:
                continue
            self.idmap_df["added_to_new_validation"][idx] = True
            row_collector.append(
                {
                    "filename": filename,
                    "int_loc": row_int_loc,
                    "startdate": constants.MIN_STARTDATE_VALIDATION,
                    "enddate": constants.MAX_ENDDATE_VALIDATION,
                }
            )
        df_new_validation_rows = pd.DataFrame(data=row_collector)
        df_new_validation_rows.drop_duplicates(keep="first", inplace=True)
        return df_new_validation_rows

    def run(self) -> List[NewValidationCsv]:
        """Argument 'df_new_validation_rows' contains all new rows for ALL validation csvs. Here we concatenate
        each row to the correct validation csv."""
        LOC_ID = "LOC_ID"
        STARTDATE = "STARTDATE"
        ENDDATE = "ENDDATE"
        collector = []
        df_new_validation_rows = self.get_new_csv_data()
        if df_new_validation_rows.empty:
            logger.debug("no new validation files to create")
            return []
        grouped_df = df_new_validation_rows.groupby("filename")
        for filename, filename_group in grouped_df:
            if filename_group.empty:
                continue
            file_path = self.fews_config.MapLayerFiles[filename]
            logger.debug(f"adding {len(filename_group)} rows to {file_path.name}")
            df = pd.read_csv(
                filepath_or_buffer=file_path,
                sep=None,
                engine="python",
            )
            assert (LOC_ID and STARTDATE and STARTDATE) in df.columns
            df.sort_values(by=list(df.columns), ascending=True, inplace=True)
            # add empty new rows to csv bottom
            for idx, row in filename_group.iterrows():
                df = df.append(
                    other={
                        LOC_ID: row.int_loc,
                        STARTDATE: row.startdate.strftime("%Y%m%d"),
                        ENDDATE: row.enddate.strftime("%Y%m%d"),
                    },
                    ignore_index=True,
                )

            new_csv = NewValidationCsv(orig_filepath=file_path, df=df)
            collector.append(new_csv)
        return collector


class HelperValidationRules:
    """
    for hoofdloc, subloc and waterstandloc this general rule applies:
        hmin <= smin < smax <= hmax
    in which:
        h = hard
        s = soft

    for waterstandloc we deal also with winter (WIN_), summer (ZOM_) and transition (OV_ in dutch 'overgang').
    for each of them the general rule applies:
        hmin <= smin < smax <= hmax
        example: WIN_HMIN <= WIN_SMIN < WIN_SMAX <= WIN_HMAX
    when comparing them (WIN, OV, and ZOM) then this applies:
        WIN <= OV <= ZOM
    """

    @classmethod
    def get_int_pars(cls, idmap_df_grouped_by_intloc: PandasDFGroupBy, int_loc: str) -> List[str]:
        try:
            int_loc_group = idmap_df_grouped_by_intloc.get_group(name=int_loc)
            int_pars = sorted(int_loc_group["internalParameter"].unique().tolist())
        except KeyError:
            int_pars = []
        return int_pars

    @classmethod
    def check_idmapping_int_loc_in_a_validation(cls, errors: Dict, idmap_df: pd.DataFrame) -> Dict:
        for idx, row in idmap_df.iterrows():
            if row["is_in_a_validation"]:
                continue
            if row["added_to_new_validation"]:
                errors["error_type"] = "not in any validation csv. Added to new csv"
                description = ""
            else:
                errors["error_type"] = "not in any validation csv. Not added to new csv"
                description = "please add manually"
            errors["internalLocation"] += [row["internalLocation"]]
            errors["start"] += [""]
            errors["eind"] += [""]
            errors["internalParameters"] += [row["internalParameter"]]
            errors["error_description"] += [
                f'{description}: exloc={row["externalLocation"]}, expar={row["externalParameter"]}'
            ]
        return errors

    @classmethod
    def check_attributes_too_few_or_many(
        cls,
        errors: Dict,
        loc_set: constants.LocationSet,
        row: pd.Series,
        int_pars: List[str],
    ) -> Dict:
        attribs_all = loc_set.get_validation_attributes(int_pars=None)
        attribs_required = loc_set.get_validation_attributes(int_pars=int_pars)
        too_few = [attrib for attrib in attribs_required if attrib not in row.keys()]
        too_many = [attrib for attrib in attribs_all if (attrib not in attribs_required) and (attrib in row.keys())]
        if too_few:
            errors = cls.__add_one_error(
                row=row, int_pars=int_pars, error_type="too_few", description=",".join(too_few), errors=errors
            )
        if too_many:
            errors = cls.__add_one_error(
                row=row, int_pars=int_pars, error_type="too_many", description=",".join(too_many), errors=errors
            )
        return errors

    @classmethod
    def _compare_two_values(
        cls, row: pd.Series, _lower: str, _upper: str, operator: str, int_pars: List[str], errors: Dict
    ) -> Dict:
        """
        add error is both values are floats and

        eval("1 > 2") --> returns False
        eval("1 <= 2") --> returns True

        """
        default_msg = f"skipping as int_loc {row['LOC_ID']}"
        try:
            value1 = float(row[_lower])
            value2 = float(row[_upper])
        except KeyError:
            logger.debug(f"{default_msg} has no field {_lower} and/or {_upper}")
            return errors
        except (ValueError, TypeError):
            logger.debug(f"{default_msg} fiels {_lower} and/or {_upper} are empty")
            # the absence is already reported in cls.check_attributes_too_few_or_many()
            return errors
        assert operator in ("<", "<=", ">", ">="), f"unexpected: unknown operator {operator}"
        if eval(f"{value1} {operator} {value2}"):
            logger.debug("skipping as two values meet condition")
            return errors
        errors = cls.__add_one_error(
            row=row, int_pars=int_pars, error_type="value", description=f"{_lower} {operator} {_upper}", errors=errors
        )
        return errors

    @classmethod
    def check_hoofd_and_sub_loc(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]) -> Dict:
        """
        hoofd- and sublocations have only 1 value for hmax, hmin, and eventually one for smax, smax
        Examples:
            hoofdlocation "H2.S." has {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}}
            sublocation "H2.R." has {"hmax": "HR2_HMAX", "hmin": "HR2_HMIN"}
            sublocation "Q.B." has {"hmax": "Q_HMAX", "smax": "Q_SMAX", "smin": "Q_SMIN", "hmin": "Q_HMIN"}
        This general rule applies:
            hmin <= smin < smax <= hmax
        in which:
            h = hard
            s = soft

        Compare values separately and only report error if both values are defined (not nan).
        """
        for statement in constants.HLOC_SLOC_VALIDATION_LOGIC:
            _lower, operator, _upper = statement
            _lower_rule = rule.get(_lower, "")  # e.g. from smin to 'HS1_HMIN'
            _upper_rule = rule.get(_upper, "")
            errors = cls._compare_two_values(
                row=row, _lower=_lower_rule, _upper=_upper_rule, operator=operator, int_pars=int_pars, errors=errors
            )
        return errors

    @classmethod
    def check_waterstandstand_loc(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]) -> Dict:
        """
        waterstandlocations have 1 value for hmax, hmin and 3 values for smax and smin
        Examples:
            waterstandloc "H.G." has {
                    "hmax": "HARDMAX",
                    "smax_win": "WIN_SMAX",
                    "smax_ov": "OV_SMAX",
                    "smax_zom": "ZOM_SMAX",
                    "smin_win": "WIN_SMIN",
                    "smin_ov": "OV_SMIN",
                    "smin_zom": "ZOM_SMIN",
                    "hmin": "HARDMIN",
                    }

        We deal with winter (WIN_), transition (OV_ in dutch 'overgang'), and summer (ZOM_).
        For each of them the general rule applies:
            hmin <= smin < smax <= hmax
            in which:
                h = hard
                s = soft
            example: WIN_HMIN <= WIN_SMIN < WIN_SMAX <= WIN_HMAX
        when comparing them (WIN, ZOM, and OV) then this applies:
            ZOM >= OV >= WIN

        Compare values separately and only report error if both values are defined (not nan).
        """
        for statement in constants.WLOC_VALIDATION_LOGIC:
            _lower, operator, _upper = statement
            _lower_rule = rule.get(_lower, "")  # e.g. from smin to 'HS1_HMIN'
            _upper_rule = rule.get(_upper, "")
            errors = cls._compare_two_values(
                row=row, _lower=_lower_rule, _upper=_upper_rule, operator=operator, int_pars=int_pars, errors=errors
            )
        return errors

    @classmethod
    def __add_one_error(
        cls, row: pd.Series, int_pars: List[str], error_type: str, description: str, errors: Dict
    ) -> Dict:
        assert isinstance(error_type, str)
        assert isinstance(description, str)
        errors["internalLocation"] += [row["LOC_ID"]]
        errors["start"] += [row["START"]]
        errors["eind"] += [row["EIND"]]
        errors["internalParameters"] += [",".join(int_pars)]
        errors["error_type"] += [error_type]
        errors["error_description"] += [description]
        return errors

    @classmethod
    def get_df_merged_validation_csvs(cls, loc_set: constants.LocationSet, fews_config: FewsConfig) -> pd.DataFrame:
        """Merge all validation csv per location set. Which validation csv must be merged is determined by:
        1) getting the attribute_file_names from RegionConfigFiles['LocationSets']
        2) getting csvfile_paths from MapLayerFiles[attribute_file_name]
        """
        assert isinstance(loc_set, constants.LocationSet)
        location_set_df = loc_set.geo_df

        merged_csv_file_names = []
        for attrib_file in loc_set.attrib_files:

            # watch out: attrib_file_name != loc_set.value.csvfile !!!
            attrib_file_name = Path(attrib_file["csvFile"]).stem
            csv_file_path = fews_config.MapLayerFiles[attrib_file_name]
            attrib_df = pd.read_csv(
                filepath_or_buffer=csv_file_path,
                sep=None,
                engine="python",
            )
            join_id = attrib_file["id"].replace("%", "")
            attrib_df.rename(columns={join_id: "LOC_ID"}, inplace=True)

            assert "END" not in attrib_df.columns, f"expected EIND, not END... {csv_file_path}"
            if ("START" and "EIND") in attrib_df.columns:
                not_okay = attrib_df[pd.to_datetime(attrib_df["EIND"]) <= pd.to_datetime(attrib_df["START"])]
                assert len(not_okay) == 0, f"EIND must be > START, {len(not_okay)} wrong rows in {attrib_file_name}"

            attribs = attrib_file["attribute"]
            if not isinstance(attrib_file["attribute"], list):
                attribs = [attribs]
            desired_attribs = [attrib.get("number", "").replace("%", "") for attrib in attribs]
            if not any(desired_attribs):
                continue
            drop_cols = [col for col in attrib_df if col not in desired_attribs + ["LOC_ID"]]
            attrib_df.drop(columns=drop_cols, axis=1, inplace=True)
            location_set_df = location_set_df.merge(attrib_df, on="LOC_ID", how="outer")
            merged_csv_file_names.append(attrib_file_name)
        logger.debug(f"merged {len(merged_csv_file_names)} csvs into {loc_set.name} validation location_set_df:")
        logger.debug(f"{merged_csv_file_names}")
        return location_set_df
