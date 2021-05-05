from mptconfig import constants
from mptconfig.checker_helpers import HelperValidationRules
from mptconfig.checker_helpers import is_in_a_validation
from mptconfig.checker_helpers import NewValidationCsv
from mptconfig.checker_helpers import NewValidationCsvCreator
from mptconfig.constants import MAX_DIFF
from mptconfig.excel import ExcelSheet
from mptconfig.excel import ExcelSheetCollector
from mptconfig.excel import ExcelSheetTypeChoices
from mptconfig.excel import ExcelWriter
from mptconfig.fews_utilities import FewsConfig
from mptconfig.fews_utilities import xml_to_dict
from mptconfig.idmapping_choices import IntLocChoices
from mptconfig.utils import flatten_nested_list
from mptconfig.utils import idmap2tags
from mptconfig.utils import is_unmeasured_location
from mptconfig.utils import pd_drop_columns
from mptconfig.utils import pd_read_csv_expect_columns
from mptconfig.utils import update_h_locs_start_end
from mptconfig.utils import update_histtag
from pathlib import Path
from shapely.geometry import Point  # noqa shapely comes with geopandas
from typing import Dict
from typing import List
from typing import Tuple

import geopandas as gpd
import logging
import numpy as np  # noqa numpy comes with geopandas
import pandas as pd  # noqa pandas comes with geopandas
import re


logger = logging.getLogger(__name__)

pd.options.mode.chained_assignment = None


class MptConfigChecker:
    """Class to read, check and write a HDSR meetpuntconfiguratie.
    The main property of the class is 'self.results' which is:
        - a dictionary of panda dataframes: each dataframe is one excel sheet.
        - updated throughout the whole class with check results
    """

    def __init__(self):
        self.results = ExcelSheetCollector()
        self._location_sets = None
        self._histtags = None
        self._hoofdloc = None
        self._hoofdloc_new = None
        self._subloc = None
        self._waterstandloc = None
        self._mswloc = None
        self._psloc = None
        self._mpt_histtags = None
        self._mpt_histtags_new = None
        self._validation_csvs_new = None
        self._fews_config = None
        self._ignored_ex_loc = None
        self._ignored_histtag = None
        self._ignored_time_series_error = None
        self._ignored_ts800 = None
        self._ignored_xy = None

    @property
    def fews_config(self):
        # why inside caching property? Since it is important to not load fews_config during
        # instantiating MptConfigChecker, as almost all tests use a patched PathConstants
        if self._fews_config is not None:
            return self._fews_config
        self._fews_config = FewsConfig(path=constants.PathConstants.fews_config.value.path)
        return self._fews_config

    @property
    def histtags(self) -> pd.DataFrame:
        if self._histtags is not None:
            return self._histtags
        logger.info(f"reading histags: {constants.PathConstants.histtags_csv.value.path}")
        dtype_columns = ["total_min_start_dt", "total_max_end_dt"]
        self._histtags = pd_read_csv_expect_columns(
            path=constants.PathConstants.histtags_csv.value.path,
            expected_columns=["serie", "total_min_start_dt", "total_max_end_dt"],
            parse_dates=dtype_columns,
        )
        for dtype_column in dtype_columns:
            if not pd.api.types.is_datetime64_dtype(self.histtags[dtype_column]):
                raise AssertionError(
                    f"dtype_column {dtype_column} in {constants.PathConstants.histtags_csv.value.path} "
                    f"can not be converted to np.datetime64. Check if values are dates."
                )
        return self._histtags

    @property
    def hoofdloc(self) -> constants.HoofdLocationSet:
        """Get HoofdLocationSet. The property .geo_df has eventually been updated."""
        if self._hoofdloc_new is not None:
            assert self._hoofdloc and isinstance(self._hoofdloc, constants.HoofdLocationSet)
            assert isinstance(self._hoofdloc_new, pd.DataFrame)
            self._hoofdloc._geo_df = self._hoofdloc_new
        if self._hoofdloc is not None:
            return self._hoofdloc
        self._hoofdloc = constants.HoofdLocationSet(fews_config=self.fews_config)
        return self._hoofdloc

    @property
    def subloc(self) -> constants.SubLocationSet:
        if self._subloc is not None:
            return self._subloc
        self._subloc = constants.SubLocationSet(fews_config=self.fews_config)
        return self._subloc

    @property
    def waterstandloc(self) -> constants.WaterstandLocationSet:
        if self._waterstandloc is not None:
            return self._waterstandloc
        self._waterstandloc = constants.WaterstandLocationSet(fews_config=self.fews_config)
        return self._waterstandloc

    @property
    def mswloc(self) -> constants.MswLocationSet:
        if self._mswloc is not None:
            return self._mswloc
        self._mswloc = constants.MswLocationSet(fews_config=self.fews_config)
        return self._mswloc

    @property
    def psloc(self) -> constants.PeilschaalLocationSet:
        if self._psloc is not None:
            return self._psloc
        self._psloc = constants.PeilschaalLocationSet(fews_config=self.fews_config)
        return self._psloc

    @property
    def mpt_histtags(self) -> pd.DataFrame:
        if self._mpt_histtags is not None:
            return self._mpt_histtags
        idmaps = self._get_idmaps()
        histtags_df = self.histtags.copy()
        histtags_df["fews_locid"] = histtags_df.apply(func=idmap2tags, args=[idmaps], axis=1)
        # nr_rows_more_than_one_loc_id = len(histtags_df[histtags_df["fews_locid"].map(len) > 1])
        # logger.debug(f"found nr_rows_more_than_one_loc_id={nr_rows_more_than_one_loc_id } which is allowed")
        histtags_df = histtags_df[histtags_df["fews_locid"].notna()]
        self._mpt_histtags = histtags_df.explode("fews_locid").reset_index(drop=True)
        return self._mpt_histtags

    @property
    def mpt_histtags_new(self) -> pd.DataFrame:
        """Convert histTag-ids to mpt-ids. Alle meetpunt ids uitgelezen uit de histTags.csv, die niet
        in de ignore staan en in de idmapping zijn opgenomen.
        mpt_histtags_new is used to create new csvs (hoofdloc, subloc, and waterstandloc) to determine
        start- and enddate.
        """
        loc_id_col = "LOC_ID"
        start_col = "STARTDATE"
        end_col = "ENDDATE"
        pd_start_col = "pd_start"
        pd_end_col = "pd_end"
        if self._mpt_histtags_new is not None:
            return self._mpt_histtags_new
        logger.debug("creating mpt_histtags_new")
        mpt_df = pd.concat(
            [
                self.mpt_histtags.groupby(["fews_locid"], sort=False)["total_min_start_dt"].min(),
                self.mpt_histtags.groupby(["fews_locid"], sort=False)["total_max_end_dt"].max(),
            ],
            axis=1,
        )
        assert sorted(mpt_df.columns) == ["total_max_end_dt", "total_min_start_dt"], "unexpected columns in mpt_df"
        assert mpt_df.index.name == "fews_locid"  # groupby() makes it the index column
        mpt_df.reset_index(drop=False, inplace=True)
        assert sorted(mpt_df.columns) == [
            "fews_locid",
            "total_max_end_dt",
            "total_min_start_dt",
        ], "unexpected columns in mpt_df"
        mpt_df.rename(
            columns={"fews_locid": loc_id_col, "total_min_start_dt": start_col, "total_max_end_dt": end_col},
            inplace=True,
        )
        kw_locs = list(mpt_df[mpt_df[loc_id_col].str.startswith("KW")][loc_id_col])
        # H_LOC ends with a 0 (e.g if subloc = KW106013, then h_loc becomes KW106010)
        h_locs = np.unique([f"{kw_loc[0:-1]}0" for kw_loc in kw_locs])
        missing_h_locs = [loc for loc in h_locs if loc not in mpt_df[loc_id_col].to_list()]
        missing_h_locs_df = pd.DataFrame(
            data={
                loc_id_col: missing_h_locs,
                start_col: [pd.NaT] * len(missing_h_locs),
                end_col: [pd.NaT] * len(missing_h_locs),
            }
        )
        mpt_df = pd.concat([mpt_df, missing_h_locs_df], axis=0)
        assert mpt_df[loc_id_col].is_unique, f"{loc_id_col} must be unique after pd.concat"
        mpt_df[[start_col, end_col]] = mpt_df.apply(
            func=update_h_locs_start_end, args=[h_locs, mpt_df], axis=1, result_type="expand"
        )
        assert mpt_df[loc_id_col].is_unique, f"{loc_id_col} must be unique after update_h_locs"
        assert not mpt_df[start_col].hasnans, f"mpt_df column {start_col} should not have nans"
        assert not mpt_df[end_col].hasnans, f"mpt_df column {end_col} should not have nans"
        mpt_df[pd_start_col] = pd.to_datetime(mpt_df[start_col], format="%Y%m%d", errors="raise")
        mpt_df[pd_end_col] = pd.to_datetime(mpt_df[end_col], format="%Y%m%d", errors="raise")
        mpt_df.drop(columns=[start_col, end_col], axis=1, inplace=True)
        self._mpt_histtags_new = mpt_df.sort_values(by=loc_id_col, ascending=True, ignore_index=True, inplace=False)
        assert sorted(self._mpt_histtags_new.columns) == [loc_id_col, pd_end_col, pd_start_col]
        return self._mpt_histtags_new

    @property
    def validation_csvs_new(self) -> List[NewValidationCsv]:
        return self._validation_csvs_new if self._validation_csvs_new else []

    @property
    def ignored_ex_loc(self) -> pd.DataFrame:
        if self._ignored_ex_loc is not None:
            return self._ignored_ex_loc
        logger.info(f"reading {constants.PathConstants.ignored_ex_loc.value.path}")
        self._ignored_ex_loc = pd_read_csv_expect_columns(
            path=constants.PathConstants.ignored_ex_loc.value.path,
            expected_columns=["externalLocation", "internalLocation"],
        )
        return self._ignored_ex_loc

    @property
    def ignored_histtag(self) -> pd.DataFrame:
        if self._ignored_histtag is not None:
            return self._ignored_histtag
        logger.info(f"reading {constants.PathConstants.ignored_histtag.value.path}")
        self._ignored_histtag = pd_read_csv_expect_columns(
            path=constants.PathConstants.ignored_histtag.value.path,
            expected_columns=["ENDDATE", "STARTDATE", "UNKNOWN_SERIE"],
        )
        self._ignored_histtag["UNKNOWN_SERIE"] = self._ignored_histtag["UNKNOWN_SERIE"].str.replace("#", "")
        return self._ignored_histtag

    @property
    def ignored_time_series_error(self) -> pd.DataFrame:
        if self._ignored_time_series_error is not None:
            return self._ignored_time_series_error
        logger.info(f"reading {constants.PathConstants.ignored_time_series_error.value.path}")
        self._ignored_time_series_error = pd_read_csv_expect_columns(
            path=constants.PathConstants.ignored_time_series_error.value.path,
            expected_columns=[
                "fout",
                "internalLocation",
                "mail datum",
                "reden om te ignoren (obv mailwisseling met CAW)",
            ],
        )
        return self._ignored_time_series_error

    @property
    def ignored_ts800(self) -> pd.DataFrame:
        if self._ignored_ts800 is not None:
            return self._ignored_ts800
        logger.info(f"reading {constants.PathConstants.ignored_ts800.value.path}")
        self._ignored_ts800 = pd_read_csv_expect_columns(
            path=constants.PathConstants.ignored_ts800.value.path,
            expected_columns=["externalLocation", "internalLocation"],
        )
        return self._ignored_ts800

    @property
    def ignored_xy(self) -> pd.DataFrame:
        if self._ignored_xy is not None:
            return self._ignored_xy
        logger.info(f"reading {constants.PathConstants.ignored_xy.value.path}")
        self._ignored_xy = pd_read_csv_expect_columns(
            path=constants.PathConstants.ignored_xy.value.path, expected_columns=["internalLocation", "x", "y"]
        )
        return self._ignored_xy

    def _update_enddate_new_csv(self, df: pd.DataFrame, file_name: str) -> pd.DataFrame:
        """Eventually update ENDDATE in new csv when it exceeds date_threshold """
        # TODO: waarom ook alweer in 1 korte zin
        date_threshold = self.mpt_histtags_new["pd_end"].max() - MAX_DIFF
        assert isinstance(date_threshold, pd.Timestamp), f"date_threshold {date_threshold} should be a pd.Timestamp"

        start_col = "START"
        end_col = "EIND"
        pd_start_col = "pd_start"
        pd_end_col = "pd_end"

        if (pd_start_col and pd_end_col) not in df.columns:
            df[pd_start_col] = pd.to_datetime(df[start_col], format="%Y%m%d", errors="coerce")
            df[pd_end_col] = pd.to_datetime(df[end_col], format="%Y%m%d", errors="coerce")

        # check which df int_locs are in self.mpt_histtags_new
        df["in_mpt_new"] = df["LOC_ID"].isin(self.mpt_histtags_new["LOC_ID"])
        df["update_this_end"] = (df["in_mpt_new"] == False) & (df[pd_end_col] > date_threshold)  # noqa
        logger.info(
            f"update {df['update_this_end'].sum()} ENDDATE in new {file_name} that "
            f"exceed date_threshold={date_threshold.strftime('%Y%m%d')}"
        )
        df.loc[df["update_this_end"] == True, pd_end_col] = constants.MAX_ENDDATE_MEASURED_LOC  # noqa
        df[start_col] = df.pd_start.dt.strftime("%Y%m%d")
        df[end_col] = df.pd_end.dt.strftime("%Y%m%d")
        df = pd_drop_columns(
            df=df, drop_columns=["in_mpt_new", pd_start_col, pd_end_col, "update_this_end", "STARTDATE", "ENDATE"]
        )
        return df

    @staticmethod
    def _df_to_csv(df: pd.DataFrame, file_name: str) -> None:
        csv_file_path = constants.PathConstants.output_dir.value.path / file_name
        if csv_file_path.suffix == "":
            csv_file_path = Path(f"{csv_file_path}.csv")
        if csv_file_path.is_file():
            logger.warning(f"overwriting existing file with path {csv_file_path}")
        df.to_csv(path_or_buf=csv_file_path.as_posix(), index=False)
        logger.info(f"created new csv {file_name}")

    @staticmethod
    def _validate_geom(gdf: gpd.GeoDataFrame) -> pd.DataFrame:
        """
        Turn a GeoDataFrame into DataFrame and:
            1. Validate geom columns names and dtypes
            2. Ensure column 'geometry' == Point('X','Y','Z')
            3. Ensure no decimal in column X, Y
        """
        assert isinstance(gdf, gpd.GeoDataFrame)
        # check column names
        assert "geometry" in gdf.columns
        assert ("X" and "Y") in gdf.columns

        # check dtypes
        assert gdf["X"].dtype in (np.float64, "float64", "O")
        assert gdf["Y"].dtype in (np.float64, "float64", "O")
        has_column_z = "Z" in gdf.columns
        if has_column_z:
            assert gdf["Z"].dtype == "O"

        # ensure geom == column(X,Y,Z)
        for idx, row in gdf.iterrows():
            assert row["geometry"].x == float(gdf["X"][idx])
            assert row["geometry"].y == float(gdf["Y"][idx])
            # if the original csv had no Z column or the Z value was missing we set it to -9999 in geometry
            assert row["geometry"].z == FewsConfig.Z_NODATA_VALUE or -50 < row["geometry"].z < 50
            if not has_column_z:
                continue
            assert row["geometry"].z == float(gdf["Z"][idx])

        # ensure no decimal in column X, Y (go from 137319.0 to 137319)
        gdf["X"] = gdf["X"].astype(np.int32)
        gdf["Y"] = gdf["Y"].astype(np.int32)
        df = gdf.drop("geometry", axis=1)
        return df

    def _write_new_opvlwater_hoofdloc_csv(self) -> None:
        """Write HoofdLocationSet.geo_df to csv. This .geo_df was eventually
        updated during check_s_loc_consistency() in _create_hoofdloc_new()."""
        if self._hoofdloc_new is None:
            logger.warning(f"skip creating {self.hoofdloc.name}.csv as hoofdloc was not updated")
            return
        logger.info(f"creating new csv {self.hoofdloc.name}")
        df = self._validate_geom(gdf=self.hoofdloc.geo_df)
        df = self._update_enddate_new_csv(df=df, file_name=self.hoofdloc.name)
        self._df_to_csv(df=df, file_name=self.hoofdloc.name)

    def _write_new_opvlwater_subloc_csv(self) -> None:
        """ Write SubLocationSet.geo_df to csv."""
        logger.info(f"creating new csv {self.subloc.name}")
        df = self._validate_geom(gdf=self.subloc.geo_df)
        df = self._update_enddate_new_csv(df=df, file_name=self.subloc.name)
        grouper = df.groupby(["PAR_ID"])
        par_types_df = grouper["TYPE"].unique().apply(func=lambda x: sorted(x)).transform(lambda x: "/".join(x))
        df["PAR_ID"] = df["LOC_ID"].str[0:-1] + "0"
        df["ALLE_TYPES"] = df["PAR_ID"].apply(func=lambda x: par_types_df.loc[x])
        df[["HBOVPS", "HBENPS"]] = df.apply(func=self._update_staff_gauge, axis=1, result_type="expand")
        # get existing fews config file name
        self._df_to_csv(df=df, file_name=self.subloc.name)

    def _write_new_waterstandlocaties_csv(self) -> None:
        """ Write WaterstandLocationSet.geo_df to csv."""
        logger.info(f"creating new csv {self.waterstandloc.name}")
        df = self._validate_geom(gdf=self.waterstandloc.geo_df)
        df = self._update_enddate_new_csv(df=df, file_name=self.waterstandloc.name)
        grouper = self.mpt_histtags.groupby(["fews_locid"])
        # leave it HIST_TAG (instead of HISTTAG), as that is what OPVLWATER_WATERSTANDEN_AUTO.csv expects
        df["HIST_TAG"] = df.apply(func=update_histtag, args=[grouper], axis=1, result_type="expand")
        self._df_to_csv(df=df, file_name=self.waterstandloc.name)

    def _write_new_validation_csvs(self) -> None:
        for new_validation_csv in self.validation_csvs_new:
            filename = new_validation_csv.orig_filepath.name
            logger.info(f"creating new csv {filename}")
            self._df_to_csv(df=new_validation_csv.df, file_name=filename)

    def _get_idmaps(self, idmap_files: List[str] = None) -> List[Dict]:
        """Get id mapping from 1 or more sources (xml files) and return them in a flatted list.
        Example:
            idmap_files = ['IdOPVLWATER', 'IdOPVLWATER_HYMOS', 'IdHDSR_NSC', 'IdOPVLWATER_WQ', 'IdGrondwaterCAW']
        returns:
            [
                ...,
                {'externalLocation': '7612', 'externalParameter': 'HB1', 'internalLocation': 'OW761202', 'internalParameter': 'H.G.0'},  # noqa
                {'externalLocation': '7612', 'externalParameter': 'HO1', 'internalLocation': 'OW761201', 'internalParameter': 'H.G.0'},  # noqa
                ...,
            ]
        """
        if not idmap_files:
            idmap_files = constants.IDMAP_FILES
        idmaps = [xml_to_dict(xml_filepath=self.fews_config.IdMapFiles[idmap])["idMap"]["map"] for idmap in idmap_files]
        return [item for sublist in idmaps for item in sublist]

    def _create_hoofdloc_new(self, par_dict: Dict) -> None:
        """Create a new hoofdloc from sublocs in case no errors found during
        check_h_loc_consistency in case all sublocs of same h_loc have consistent parameters."""
        assert isinstance(par_dict, dict), f"par_dict should be a dictionary, not a {type(par_dict)}"
        par_gdf = pd.DataFrame(data=par_dict)
        columns = list(self.hoofdloc.geo_df.columns)
        drop_cols = [col for col in columns if col in par_gdf.columns and col != "LOC_ID"]
        new_geo_df = self.hoofdloc.geo_df.drop(drop_cols, axis=1, inplace=False)
        new_geo_df = par_gdf.merge(new_geo_df, on="LOC_ID")
        new_geo_df["geometry"] = new_geo_df.apply(
            func=lambda x: Point(float(x["X"]), float(x["Y"]), float(x["Z"])), axis=1
        )
        new_geo_df = new_geo_df[columns]
        self._hoofdloc_new = gpd.GeoDataFrame(new_geo_df)

    def _update_staff_gauge(self, row: pd.Series) -> Tuple[str, str]:
        """Assign upstream and downstream staff gauges to subloc."""
        result = {"HBOV": "", "HBEN": ""}
        for key in result.keys():
            df = self.waterstandloc.geo_df.loc[self.waterstandloc.geo_df["LOC_ID"] == row[key]]
            if not df.empty:
                result[key] = df["PEILSCHAAL"].values[0]
        return result["HBOV"], result["HBEN"]

    def check_idmap_int_loc_in_csv(self, sheet_name: str = "idmap int_loc in csv error") -> ExcelSheet:
        """Check if IdOPVLWATER.xml int_locs are in correct (hoofdloc/subloc/ow) csv."""
        description = (
            "Elke IdOPVLWATER.xml int_loc moet 1x voorkomen in juiste mpt csv (hoofd/sub/ow/msw). "
            "Int_loc type wordt bepaald obv int_loc string eg 'KW761234'"
        )
        logger.info(f"start {self.check_idmap_int_loc_in_csv.__name__} with sheet_name={sheet_name}")

        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        errors = {
            "int_locs": [],
            "error_type": [],
        }
        idmap_df = pd.DataFrame(data=idmaps)
        idmap_df["is_ow"] = idmap_df["internalLocation"].apply(func=lambda x: IntLocChoices.is_ow(x))
        idmap_df["is_kw_hoofd"] = idmap_df["internalLocation"].apply(func=lambda x: IntLocChoices.is_kw_hoofd(x))
        idmap_df["is_kw_sub"] = idmap_df["internalLocation"].apply(func=lambda x: IntLocChoices.is_kw_sub(x))
        idmap_df["is_msw"] = idmap_df["internalLocation"].apply(func=lambda x: IntLocChoices.is_msw(x))
        # hoofd locations are in oppvlwater_hoofdloc.csv
        idmap_df["in_hoofd_csv"] = idmap_df["internalLocation"].isin(self.hoofdloc.geo_df["LOC_ID"])
        # sub locations are in oppvlwater_subloc.csv
        idmap_df["in_sub_csv"] = idmap_df["internalLocation"].isin(self.subloc.geo_df["LOC_ID"])
        # ow locations are in oppvlwater_waterstanden.csv
        idmap_df["in_ow_csv"] = idmap_df["internalLocation"].isin(self.waterstandloc.geo_df["LOC_ID"])
        # msw locations are in msw_stations.csv
        idmap_df["in_msw_csv"] = idmap_df["internalLocation"].isin(self.mswloc.geo_df["LOC_ID"])
        idmap_df["nr_in_a_csv"] = sum(
            [idmap_df["in_hoofd_csv"], idmap_df["in_sub_csv"], idmap_df["in_ow_csv"], idmap_df["in_msw_csv"]]
        )

        # check 1: not in csv at all
        df1 = idmap_df[idmap_df["nr_in_a_csv"] == 0]
        if not df1.empty:
            int_locs_not_in_any_csv = df1["internalLocation"].to_list()
            errors["int_locs"] += int_locs_not_in_any_csv
            errors["error_type"] += ["not in any csv"] * len(int_locs_not_in_any_csv)

        # check 2: in multiple csvs
        df2 = idmap_df[idmap_df["nr_in_a_csv"] > 1]
        if not df2.empty:
            int_locs_in_multi_csv = df2["internalLocation"].to_list()
            errors["int_locs"] += int_locs_in_multi_csv
            errors["error_type"] += ["in multiple csvs"] * len(int_locs_in_multi_csv)

        # check 3: hoofd in sub/ow/msw csv
        df3 = idmap_df[
            (idmap_df["is_kw_hoofd"] == True)  # noqa
            & ((idmap_df["in_sub_csv"] == True) | (idmap_df["in_ow_csv"] == True) | (idmap_df["in_msw_csv"] == True))
        ]
        if not df3.empty:
            int_locs_hoofd_wrong = df3["internalLocation"].to_list()
            errors["int_locs"] += int_locs_hoofd_wrong
            errors["error_type"] += ["hoofd in wrong csv"] * len(int_locs_hoofd_wrong)

        # check 4: sub in hoofd/ow/msw csv
        df4 = idmap_df[
            (idmap_df["is_kw_sub"] == True)  # noqa
            & ((idmap_df["in_hoofd_csv"] == True) | (idmap_df["in_ow_csv"] == True) | (idmap_df["in_msw_csv"] == True))
        ]
        if not df4.empty:
            int_locs_sub_wrong = df4["internalLocation"].to_list()
            errors["int_locs"] += int_locs_sub_wrong
            errors["error_type"] += ["sub in wrong csv"] * len(int_locs_sub_wrong)

        # check 5: ow in hoofd/sub/msw csv
        df5 = idmap_df[
            (idmap_df["is_ow"] == True)  # noqa
            & ((idmap_df["in_hoofd_csv"] == True) | (idmap_df["in_sub_csv"] == True) | (idmap_df["in_msw_csv"] == True))
        ]
        if not df5.empty:
            int_locs_ow_wrong = df5["internalLoctation"].to_list()
            errors["int_locs"] += int_locs_ow_wrong
            errors["error_type"] += ["ow in wrong csv"] * len(int_locs_ow_wrong)

        # check 6: msw in hoofd/sub/ow csv
        df6 = idmap_df[
            (idmap_df["is_msw"] == True)  # noqa
            & ((idmap_df["in_hoofd_csv"] == True) | (idmap_df["in_sub_csv"] == True) | (idmap_df["in_ow_csv"] == True))
        ]
        if not df6.empty:
            int_locs_msw_wrong = df6["internalLocation"].to_list()
            errors["int_locs"] += int_locs_msw_wrong
            errors["error_type"] += ["msw in wrong csv"] * len(int_locs_msw_wrong)

        result_df = pd.DataFrame(data=errors)
        if result_df.empty:
            logger.info("all idmaps int_locs in correct csv")
        else:
            logger.warning(f"{len(result_df)} idmaps int_locs not in any/correct csv")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_dates_loc_sets(self, sheet_name: str = "loc_set date errors") -> ExcelSheet:
        description = (
            f"datums moet in logische range vallen {constants.MIN_DATE_ALLOWED.strftime('%Y%m%d')}-"
            f"{constants.MIN_DATE_ALLOWED.strftime('%Y%m%d')}. Onbemeten locatie moet beide dummy datums "
            f"hebben. START moet eerder dan EIND zijn."
        )
        logger.info(f"start {self.check_dates_loc_sets.__name__} with sheet_name={sheet_name}")

        date_errors = {"internalLocation": [], "error_type": [], "error": []}
        start_col = "START"
        end_col = "EIND"
        pd_start_col = "pd_start"
        pd_end_col = "pd_end"
        assert (start_col and end_col) not in self.mswloc.geo_df.columns
        for loc_set in (self.hoofdloc, self.subloc, self.waterstandloc, self.psloc):
            assert (start_col and end_col and "LOC_ID") in loc_set.geo_df.columns
            df = loc_set.geo_df
            df[pd_start_col] = pd.to_datetime(df[start_col], format="%Y%m%d", errors="coerce")
            df[pd_end_col] = pd.to_datetime(df[end_col], format="%Y%m%d", errors="coerce")

            # check 1: can dates be converted?
            # find all rows where nans (pd.to_datetime unsuccessful): save row as error and drop row
            for col in (pd_start_col, pd_end_col):
                if not df[col].hasnans:
                    continue
                for idx, row in df.iterrows():
                    if not pd.isna(row[col]):
                        continue
                    date_errors["internalLocation"] += [row["LOC_ID"]]
                    date_errors["error_type"] += ["conversion"]
                    date_errors["error"] += [f"start={row[start_col]}, end={row[end_col]}"]
                # drop rows, continue where row notna
                df = df[df[col].notna()]

            # check 2: measured vs unmeasured
            # if startdate indicates a unmeasured location, then enddate must do also (and vice-versa)
            df["start_is_unmeasured"] = df[pd_start_col] == constants.STARTDATE_UNMEASURED_LOC
            df["end_is_unmeasured"] = df[pd_end_col] == constants.ENDDATE_UNMEASURED_LOC
            if any(df[df["start_is_unmeasured"] != df["end_is_unmeasured"]]):
                for idx, row in df.iterrows():
                    if row["start_is_unmeasured"] == row["end_is_unmeasured"]:
                        continue
                    date_errors["internalLocation"] += [row["LOC_ID"]]
                    date_errors["error_type"] += ["unmeasured loc?"]
                    date_errors["error"] += [f"start={row[start_col]}, end={row[end_col]}"]
                # drop rows, continue only where 2 cols are equal
                df = df[df["start_is_unmeasured"] == df["end_is_unmeasured"]]

            # check 3: startdate must be smaller then or equal to enddate
            df["wrong order"] = df[pd_start_col] > df[pd_end_col]
            if any(df["wrong order"]):
                for idx, row in df.iterrows():
                    if not row["wrong order"]:
                        continue
                    date_errors["internalLocation"] += [row["LOC_ID"]]
                    date_errors["error_type"] += ["wrong order"]
                    date_errors["error"] += [f"start={row[start_col]}, end={row[end_col]}"]

            # check 4: dates in allowed range?
            # start in allowed range?
            df_start_is_outside = df[
                (df[pd_start_col] < constants.MIN_DATE_ALLOWED) | (df[pd_start_col] > constants.MAX_DATE_ALLOWED)
            ]
            if not df_start_is_outside.empty:
                for idx, row in df.iterrows():
                    if not row["start_is_unmeasured"]:
                        # only wrong if it not a unmeasured location
                        continue
                    date_errors["internalLocation"] += [row["LOC_ID"]]
                    date_errors["error_type"] += ["start out of range date"]
                    date_errors["error"] += [f"start={row[start_col]}, end={row[end_col]}"]
            # end in allowed range?
            df_end_is_outside = df[
                (df[pd_end_col] < constants.MIN_DATE_ALLOWED) | (df[pd_end_col] > constants.MAX_DATE_ALLOWED)
            ]
            if not df_end_is_outside.empty:
                for idx, row in df.iterrows():
                    if not row["end_is_unmeasured"]:
                        # only wrong if it not a unmeasured location
                        continue
                    date_errors["internalLocation"] += [row["LOC_ID"]]
                    date_errors["error_type"] += ["end out of range date"]
                    date_errors["error"] += [f"start={row[start_col]}, end={row[end_col]}"]
            df = pd_drop_columns(df=df, drop_columns=["start_is_unmeasured", "end_is_unmeasured", "wrong_order"])

        result_df = pd.DataFrame(data=date_errors)
        if result_df.empty:
            logger.info("now wrong dates found")
        else:
            logger.warning(f"{len(result_df)} wrong dates found")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_idmap_sections(self, sheet_name: str = "idmap section error") -> ExcelSheet:
        """Check if all KW/OW locations are in the correct section."""
        description = "Idmaps die niet in de juiste sectie zijn opgenomen"
        logger.info(f"start {self.check_idmap_sections.__name__} with sheet_name={sheet_name}")
        result_df = pd.DataFrame(
            columns=["bestand", "externalLocation", "externalParameter", "internalLocation", "internalParameter"]
        )
        for idmap, subsecs in constants.IDMAP_SECTIONS.items():
            xml_filepath = self.fews_config.IdMapFiles[idmap]
            for section_type, sections in subsecs.items():
                for section in sections:
                    section_start = section.get("section_start", "")
                    section_end = section.get("section_end", "")
                    _dict = xml_to_dict(xml_filepath=xml_filepath, section_start=section_start, section_end=section_end)
                    idmapping = _dict["idMap"]["map"]
                    prefix = constants.SECTION_TYPE_PREFIX_MAPPER[section_type]
                    pattern = fr"{prefix}\d{{6}}$"
                    idmap_wrong_section = [
                        idmap
                        for idmap in idmapping
                        if not bool(re.match(pattern=pattern, string=idmap["internalLocation"]))
                    ]
                    if not idmap_wrong_section:
                        continue
                    logger.warning(
                        (
                            f"{len(idmap_wrong_section)} "
                            f"internalLocations not {prefix}XXXXXX "
                            f"between {section_start} and {section_end} "
                            f"in {idmap}."
                        )
                    )
                    df = pd.DataFrame(data=idmap_wrong_section)
                    df["sectie"] = section_start  # e.g. '<!--KUNSTWERK SUBLOCS (new CAW id)-->'
                    df["bestand"] = idmap  # e.g 'IdOPVLWATER'
                    result_df = pd.concat(objs=[result_df, df], axis=0, join="outer")
        if result_df.empty:
            logger.info("found no idmap section errors")
        else:
            logger.warning(f"{len(result_df)} idmap section errors found")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_ignored_histtags(
        self,
        sheet_name: str = "ignored histtags match",
        idmap_files: List[str] = None,
    ) -> ExcelSheet:
        """Check if ignored histTags do match with idmap."""
        description = "hisTags uit de histTag_ignore die wél in de idmaps zijn opgenomen"
        logger.info(f"start {self.check_ignored_histtags.__name__} with sheet_name={sheet_name}")
        assert isinstance(idmap_files, List) if idmap_files else True, "idmap_files must be a List"
        if not idmap_files:
            idmap_files = ["IdOPVLWATER"]
        histtags_opvlwater_df = self.histtags.copy()
        idmaps = self._get_idmaps(idmap_files=idmap_files)
        # TODO: @daniel kan fews_locid een lijst met meerdere loc_id's zijn?
        #  histtags_opvlwater_df.fews_locid.dtype is 'O' (is al string)
        #  daniel: "Met uitzondering van de functie mpt_histtags niet. In
        #  property 'mpt_histtags' wordt deze lijst geexplodeerd".
        histtags_opvlwater_df["fews_locid"] = self.histtags.apply(func=idmap2tags, args=[idmaps], axis=1)

        # df_rows_more_than_one_loc_id = histtags_opvlwater_df[histtags_opvlwater_df["fews_locid"].map(len) > 1]
        # if len(df_rows_more_than_one_loc_id) > 0:
        #     pass
        # nr_wrong = len(df_rows_more_than_one_loc_id)
        # TODO: @daniel2: alleen mpt_histtags kan meerdere fews_locid (lijst met >1 elementen) hebben toch?
        #  hier nr_wrong = 30
        #  @renier: Ik denk niet dat er iets niet klopt; óf de lijst wordt exploded, wanneer de fews_locid
        #  zelf relevant is, óf er wordt alleen gekeken of de apply-method niet een nan terug geeft.
        # example = df_rows_more_than_one_loc_id.iloc[1]
        # raise AssertionError(
        #     f"unexpected: nr_rows_gte_one_loc_id={nr_wrong}, "
        #     f"example: serie={example.serie}, fews_locid={example.fews_locid}"
        # )
        # T

        histtags_opvlwater_df = histtags_opvlwater_df[histtags_opvlwater_df["fews_locid"].notna()]
        result_df = self.ignored_histtag[
            self.ignored_histtag["UNKNOWN_SERIE"].isin(values=histtags_opvlwater_df["serie"])
        ]
        if result_df.empty:
            logger.info("hisTags ignore list consistent with idmaps")
        else:
            logger.warning(f"{len(result_df)} histTags should not be in ignored histtags")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_histtags_nomatch(self, sheet_name: str = "histtags nomatch") -> ExcelSheet:
        """Check if hisTags can be mapped to internal location (if there are not included in histtag_ignore list)"""
        description = (
            "hisTags die niet konden worden gemapped naar interne locatie en niet in de hisTag_ignore zijn opgenomen"
        )
        logger.info(f"start double{self.check_histtags_nomatch.__name__} with sheet_name={sheet_name}")
        histtags_df = self.histtags.copy()
        idmaps = self._get_idmaps()
        histtags_df["fews_locid"] = self.histtags.apply(func=idmap2tags, args=[idmaps], axis=1)

        # df_rows_more_than_one_loc_id = histtags_df[histtags_df["fews_locid"].map(len) > 1]
        # if len(df_rows_more_than_one_loc_id) > 0:
        #     pass
        # nr_wrong = len(df_rows_more_than_one_loc_id)
        # TODO: @daniel2: alleen mpt_histtags kan meerdere fews_locid (lijst met >1 elementen) hebben toch?
        #  @renier: Ik denk niet dat er iets niet klopt; óf de lijst wordt exploded, wanneer de fews_locid
        #  zelf relevant is, óf er wordt alleen gekeken of de apply-method niet een nan terug geeft.
        # example = df_rows_more_than_one_loc_id.iloc[1]
        # raise AssertionError(
        #     f"unexpected: nr_rows_gte_one_loc_id={nr_wrong}, "
        #     f"example: serie={example.serie}, fews_locid={example.fews_locid}"
        # )

        result_df = histtags_df[histtags_df["fews_locid"].isna()]
        result_df = result_df[~result_df["serie"].isin(values=self.ignored_histtag["UNKNOWN_SERIE"])]
        result_df = result_df.drop("fews_locid", axis=1)
        result_df.columns = ["UNKNOWN_SERIE", "STARTDATE", "ENDDATE"]
        if result_df.empty:
            logger.info("all histTags in idMaps")
        else:
            logger.warning(f"{len(result_df)} histTags not in idMaps")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_double_idmaps(self, sheet_name: str = "idmaps double") -> ExcelSheet:
        """Check if identical idmaps are doubled."""
        # roger: volgens mij is dit (maar dat weet ik niet zeker):
        #   histtags mag alleen worden aangeboden als 3 cijferig, als 4 cijferig en als 800 locatie

        # roger:
        # als idmaps
        # bepaalde histtags mogen slechts aan 1 interne locaties parameters combinaties zijn gekoppeld
        #   - een krooshekpeil kan maar aan 1 sublocatie
        #   - een stuurpeil of streefpeil kan wel aan meerdere
        # als het goed gebruikt deze check een whitelist (uitzondering, deze parameter typen wel, deze niet)
        # renier:
        # dat gebeurt niet hier Roger! :)

        description = "idmaps die dubbel in de dubbel gedefinieerd staan in de idmap-files"
        logger.info(f"start {self.check_double_idmaps.__name__} with sheet_name={sheet_name}")
        result_df = pd.DataFrame(
            columns=["bestand", "externalLocation", "externalParameter", "internalLocation", "internalParameter"]
        )
        for idmap_file in constants.IDMAP_FILES:
            idmaps = self._get_idmaps(idmap_files=[idmap_file])
            idmap_doubles = [idmap for idmap in idmaps if idmaps.count(idmap) > 1]
            if not idmap_doubles:
                logger.info(f"No double idmaps in {idmap_file} ")
                continue
            idmap_doubles = list({idmap["externalLocation"]: idmap for idmap in idmap_doubles}.values())
            logger.warning(f"{len(idmap_doubles)} double idmaps in {idmap_file}")
            df = pd.DataFrame(
                data=idmap_doubles,
                columns=["internalLocation", "externalLocation", "internalParameter", "externalParameter"],
            )
            df["bestand"] = idmap_file
            result_df = pd.concat(objs=[result_df, df], axis=0, join="outer")
        if result_df.empty:
            logger.info("no double idmaps found")
        else:
            logger.warning(f"found {len(result_df)} double idmaps")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_missing_pars(self, sheet_name: str = "pars missing") -> ExcelSheet:
        """Check if internal parameters in idmaps are missing in parameters.xml.
        All id_mapping.xml inpars (e.g. ‘H.R.0’) must exists in RegionConfigFiles/parameters.xml"""
        description = "controle of interne parameters missen in paramters.xml"
        logger.info(f"start {self.check_missing_pars.__name__} with sheet_name={sheet_name}")
        config_parameters = list(self.fews_config.get_parameters(dict_keys="parameters").keys())

        idmaps = self._get_idmaps()
        id_map_parameters = [id_map["internalParameter"] for id_map in idmaps]
        params_missing = [parameter for parameter in id_map_parameters if parameter not in config_parameters]

        result_df = pd.DataFrame(data={"parameters": params_missing})
        if result_df.empty:
            logger.info("all internal paramters are in config")
        else:
            logger.warning(f"{len(result_df)} parameter(s) in idMaps are missing in config")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_s_loc_consistency(self, sheet_name: str = "s_locs not consistent") -> ExcelSheet:
        """Check if all sub_locs of the same h_loc have consistent parameters: xy, rayon, systeem, kompas."""
        description = "fouten in CAW sublocatie-groepen waardoor hier geen hoofdlocaties.csv uit kan worden geschreven"
        logger.info(f"start {self.check_s_loc_consistency.__name__} with sheet_name={sheet_name}")

        h_loc_errors = {
            "LOC_ID": [],
            "SUB_LOCS": [],
            "LOC_NAME": [],
            "GEOMETRY": [],
            "SYSTEEM": [],
            "RAYON": [],
            "KOMPAS": [],
        }

        grouper = self.subloc.geo_df.groupby("PAR_ID")
        par_dict = {
            "LOC_ID": [],
            "LOC_NAME": [],
            "X": [],
            "Y": [],
            "ALLE_TYPES": [],
            "START": [],
            "EIND": [],
            "SYSTEEM": [],
            "RAYON": [],
            "KOMPAS": [],
        }

        for loc_id, gdf in grouper:
            caw_code = loc_id[2:-2]
            errors = dict.fromkeys(["LOC_NAME", "GEOMETRY", "SYSTEEM", "RAYON", "KOMPAS"], False)
            fields = dict.fromkeys(par_dict.keys(), None)
            fields["LOC_ID"] = loc_id

            loc_names = np.unique(gdf["LOC_NAME"].str.extract(pat=f"([A-Z0-9 ]*_{caw_code}-K_[A-Z0-9 ]*)").values)

            if len(loc_names) == 1:
                fields["LOC_NAME"] = loc_names[0]
            else:
                errors["LOC_NAME"] = ",".join(loc_names)

            if any([re.match(pattern=loc, string=loc_id) for loc in self.ignored_xy["internalLocation"]]):
                fields["X"], fields["Y"] = next(
                    [row["x"], row["y"]]
                    for index, row in self.ignored_xy.iterrows()
                    if re.match(pattern=row["internalLocation"], string=loc_id)
                )

            else:
                geoms = gdf["geometry"].unique()
                if len(geoms) == 1:
                    fields["X"] = geoms[0].x
                    fields["Y"] = geoms[0].y
                else:
                    errors["GEOMETRY"] = ",".join([f"({geom.x} {geom.y})" for geom in geoms])

            all_types = list(gdf["TYPE"].unique())
            all_types.sort()
            fields["ALLE_TYPES"] = "/".join(all_types)
            fields["START"] = gdf["START"].min()
            fields["EIND"] = gdf["EIND"].max()
            for attribuut in ["SYSTEEM", "RAYON", "KOMPAS"]:
                vals = gdf[attribuut].unique()
                if len(vals) == 1:
                    fields[attribuut] = vals[0]
                else:
                    errors[attribuut] = ",".join(vals)

            if None not in fields.values():
                for key, value in fields.items():
                    par_dict[key].append(value)

            if any(errors.values()):
                h_loc_errors["LOC_ID"].append(loc_id)
                h_loc_errors["SUB_LOCS"].append(",".join(gdf["LOC_ID"].values))
                for key, value in errors.items():
                    if value is False:
                        value = ""
                    h_loc_errors[key].append(value)

        result_df = pd.DataFrame(data=h_loc_errors)
        if result_df.empty:
            logger.info("all grouped sublocs are consistent with eachother (xy, rayon, etc)")
            self._create_hoofdloc_new(par_dict=par_dict)
        else:
            logger.warning(f"{len(result_df)} grouped sublocs are not consistent with eachother (xy, rayon, etc)")
            logger.warning("h_locs can only be re-written when consistency errors are resolved")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_ex_par_errors_int_loc_missing(
        self, ex_par_sheet_name: str = "ex_par error", int_loc_sheet_name: str = "int_loc missing"
    ) -> Tuple[ExcelSheet, ExcelSheet]:
        """Check on wrong external parameters and missing internal locations. This check returns
        two sheets (2x name+df), whereas all other checks return one sheet (1x name+df)."""

        # roger: = ik snap eigenlijk niet waarom de kolom SS/SM erin staat.
        # De bedoeling was dat als een schuif wel een ES heeft, maar geen SP of SS of SM, dat het dan vreemd is.
        # Als een schuif geen ES heeft, maar wel een SP of SS of SM heeft, is het ook vreemd.
        # renier:
        # S.S = schuifstand (mNAP)
        # S.M = schuifstand (m tov onderkant of bovenkant oid)
        # S.W = stuwstand
        # S.P = openingspercentage

        # IX. (in bedrijf)
        # IB.0 	    in bedrijf noneq                                    bijv IB2.0
        # IBH.0     in bedrijf hoogtoeren [-] noneq                     bijv IBH2.0
        # IBL.0	    in bedrijf laagtoeren [-] noneq                     bijv IBL2.0

        # I.X (draaiduur)
        # DD.15     draaiduur aantal seconden per 15min (dus max 900)
        # DD.h      draaiduur aantal seconden per uur (dus max 3600)
        # DDL.15    draaiduur laagtoeren sec per 15 min
        # DDH.15    draaiduur hoogtoeren sec per 15 min
        #   renier:
        #   - noneq komt niet voor (DD.0, DDl.0, DDH.0).
        #   - ik zie ook niet DD1.xx of DD.1.xx, of DD2.xx of DD.2.xx oid

        # KW218221 komt hier naar boven: een afsluiter met een Q1. Echter, afsluiters hebben geen debiet, die
        # hebben 0 of 1. Echter KW218221 is een uitzondering. We zouden een ignore voor KW218221 (alleen voor SM/SS
        # kunnen maken.. lage prio)

        ex_par_description = "locaties waar foute externe parameters aan zijn gekoppeld"
        int_loc_description = "interne locaties in de idmap die niet zijn opgenomen in locatiesets"

        logger.info(
            f"start {self.check_ex_par_errors_int_loc_missing.__name__} with 2 "
            f"sheet_names={ex_par_sheet_name} and {int_loc_sheet_name}"
        )

        ex_par_errors = {
            "internalLocation": [],
            "locationType": [],
            "ex_par_error": [],
            "types": [],
            "FQ": [],
            "I.X": [],
            "IX.": [],
            "SS./SM.": [],
        }
        int_loc_missing = []
        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)
        for int_loc, loc_group in idmap_df.groupby("internalLocation"):
            regexes = []
            errors = dict.fromkeys(["I.X", "IX.", "FQ", "SS./SM."], False)
            ex_pars = np.unique(loc_group["externalParameter"].values)
            ex_pars_gen = [re.sub(r"\d", ".", ex_par) for ex_par in ex_pars]
            if int_loc in self.hoofdloc.geo_df["LOC_ID"].values:
                loc_properties = self.hoofdloc.geo_df[self.hoofdloc.geo_df["LOC_ID"] == int_loc]
                loc_type = "hoofdloc"
            elif int_loc in self.subloc.geo_df["LOC_ID"].values:
                loc_properties = self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == int_loc]
                loc_type = "subloc"
                regexes = ["HR.$"]
            elif int_loc in self.waterstandloc.geo_df["LOC_ID"].values:
                loc_type = "waterstandloc"
            elif int_loc in self.mswloc.geo_df["LOC_ID"].values:
                loc_type = "mswloc"
            else:
                loc_type = None
                int_loc_missing += [int_loc]
            if loc_type in ["hoofdloc", "subloc"]:
                all_types = loc_properties["ALLE_TYPES"].values[0].split("/")
                all_types = [item.lower() for item in all_types]
            elif loc_type == "waterstandloc":
                all_types = ["waterstandloc"]

            if loc_type == "subloc":
                sub_type = self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == int_loc]["TYPE"].values[0]

                allowed_parameters = [
                    parameters
                    for _type, parameters in constants.EXTERNAL_PARAMETERS_ALLOWED.items()
                    if _type in all_types
                ]
                regexes += flatten_nested_list(_list=allowed_parameters)

                ex_par_error = [
                    ex_par
                    for ex_par in ex_pars
                    if not any([regex.match(ex_par) for regex in [re.compile(rex) for rex in regexes]])
                ]

                if sub_type == "schuif":
                    if not any([ex_par for ex_par in ex_pars_gen if ex_par in ["SS.", "SM.", "SP."]]):
                        errors["SS./SM."] = True

                if any([ex_par for ex_par in ex_pars_gen if ex_par in ["I.B", "I.H", "I.L"]]):
                    if not any([ex_par for ex_par in ex_pars_gen if ex_par in ["IB.", "IH.", "IL."]]):
                        errors["IX."] = True

                elif any([ex_par for ex_par in ex_pars_gen if ex_par in ["IB.", "IH.", "IL."]]):
                    errors["I.X"] = True

                if "FQ." in ex_pars_gen:
                    if not any(
                        [ex_par for ex_par in ex_pars_gen if ex_par in ["IB.", "IH.", "IL.", "I.B", "I.H", "I.L"]]
                    ):
                        errors["FQ"] = True

            elif loc_type == "hoofdloc":
                regexes = ["HS.$", "QR.$", "QS.$", "WR", "WS"]
                ex_par_error = [
                    ex_par
                    for ex_par in ex_pars
                    if not any([regex.match(ex_par) for regex in [re.compile(rex) for rex in regexes]])
                ]

            else:
                ex_par_error = []

            # TODO: if ex_par_errors results is weird then look at this:
            #  daniel used bitwise operator |, but I'm not sure if that is what he meant...
            #  suppose:
            #  len(ex_par_error) > 0  # True
            #  any(errors.values()) # False
            #  then:
            #  len(ex_par_error) > 0 or any(errors.values()) # True
            #  len(ex_par_error) > 0 | any(errors.values()) # False !!
            #  while:
            #  True or False # True
            #  True | False # True
            #  this has to do with

            # TODO: renier will use 'or' instead of bitwise | ..
            if len(ex_par_error) > 0 or any(errors.values()):
                ex_par_errors["internalLocation"].append(int_loc)
                ex_par_errors["locationType"].append(loc_type)
                ex_par_errors["ex_par_error"].append(",".join(ex_par_error))
                ex_par_errors["types"].append(",".join(all_types))
                for key, value in errors.items():
                    ex_par_errors[key].append(value)

        # Roger:
        # niet veranderen, maar wel sidenote bij interpreteren van result_df:
        # 1) laatste vier kolomen van ex_par_result_df ("FQ", "I.X", "IX", "SS./SM) zijn niet
        #    beetje raar op het eerste zicht:
        #    eerste 3 zijn nl niet relevant als types == schuif
        # 2) als true in 1 vd laatste 4 kolommen, hoe dan oplossen:
        #    voorbeeld:
        #       internalLocation               KW109711
        #       locationType                     subloc
        #       ex_par_error
        #       types               krooshek,pompvijzel
        #       FQ                                False
        #       I.X                                True
        #       IX.                               False
        #       SS./SM.                           False
        #       Name: 13, dtype: object
        #    oplossing: ga naar IdMapFiles/IdOPVLWATER.xml en zoek KW109711, geeft:
        #    	<map externalLocation="097" externalParameter="HR1" internalLocation="KW109711" internalParameter="H.R.0"/>  # noqa
        #    	<map externalLocation="097" externalParameter="IB1" internalLocation="KW109711" internalParameter="IB.0"/>   # noqa
        #    	<map externalLocation="097" externalParameter="Q1" internalLocation="KW109711" internalParameter="Q.G.0"/>   # noqa
        #    er mist dus een
        #    	<map externalLocation="097" externalParameter="I1B" internalLocation="KW109711" internalParameter="DD.15"/>     # noqa
        #    als je die regel toevoegt, en checker opnieuw draait dan krijg je ws error dat hiervoor geen tijdserie beschikbaar is,     # noqa
        #    dus dan moeten we deze toevoegen aan een ignore lijst.
        # 3) als er een openingspercentage is, dan is het niet erg dan er een SS of SM ontbreekt

        ex_par_result_df = pd.DataFrame(data=ex_par_errors)
        int_loc_result_df = pd.DataFrame(data={"internalLocation": int_loc_missing})

        if len(ex_par_result_df) == 0:
            logger.info("no external parameter errors")
        else:
            logger.warning(f"{len(ex_par_result_df)} locations with external parameter errors")

        if len(int_loc_result_df) == 0:
            logger.info("all internal locations are in locationSets")
        else:
            logger.warning(f"{len(int_loc_result_df)} internal locations are not in locationSets")

        ex_par_sheet = ExcelSheet(
            name=ex_par_sheet_name,
            description=ex_par_description,
            df=ex_par_result_df,
            sheet_type=ExcelSheetTypeChoices.output_check,
        )
        int_loc_sheet = ExcelSheet(
            name=int_loc_sheet_name,
            description=int_loc_description,
            df=int_loc_result_df,
            sheet_type=ExcelSheetTypeChoices.output_check,
        )
        return ex_par_sheet, int_loc_sheet

    def check_ex_par_missing(self, sheet_name: str = "ex_par missing") -> ExcelSheet:
        """Check if external parameters are missing on locations."""
        description = "locaties waar externe parameters missen"
        logger.info(f"start {self.check_ex_par_missing.__name__} with sheet_name={sheet_name}")
        ex_par_missing = {
            "internalLocation": [],
            "ex_pars": [],
            "QR": [],
            "QS": [],
            "HS": [],
        }
        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)
        for index, row in self.hoofdloc.geo_df.iterrows():
            missings = dict.fromkeys(["QR", "QS", "HS"], False)
            int_loc = row["LOC_ID"]
            loc_group = idmap_df[idmap_df["internalLocation"] == int_loc]
            if loc_group.empty:
                ex_pars = []
                ex_pars_gen = []
            else:
                ex_pars = np.unique(ar=loc_group["externalParameter"].values)
                ex_pars_gen = [re.sub(pattern=r"\d", repl=".", string=ex_par) for ex_par in ex_pars]
            if "HS." not in ex_pars_gen:
                missings["HS"] = True
            if "QR." not in ex_pars_gen:
                missings["QR"] = True
            if "QS." not in ex_pars_gen:
                missings["QS"] = True
            if any(missings.values()):
                ex_par_missing["internalLocation"].append(int_loc)
                ex_par_missing["ex_pars"].append(",".join(ex_pars))
                for key, value in missings.items():
                    ex_par_missing[key].append(value)

        result_df = pd.DataFrame(data=ex_par_missing)
        if len(result_df) == 0:
            logger.info("No external parameters missing")
        else:
            logger.warning(f"{len(result_df)} locations with external parameter missing")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_ex_loc_int_loc_mismatch(self, sheet_name: str = "ex_loc int_loc mismatch") -> ExcelSheet:
        """Check if external locations are consistent with internal locations."""
        description = "externe locaties die niet passen bij interne locatie"
        logger.info(f"start {self.check_ex_loc_int_loc_mismatch.__name__} with sheet_name={sheet_name}")
        ex_loc_errors = {"internalLocation": [], "externalLocation": []}
        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)
        for loc_group in idmap_df.groupby("externalLocation"):
            int_loc_error = []
            ex_loc = loc_group[0]
            assert isinstance(ex_loc, str) and len(ex_loc) in (3, 4), "we expected ex_loc is str with length 3 or 4"
            int_locs = np.unique(loc_group[1]["internalLocation"].values)
            if len(ex_loc) == 3:
                if bool(re.match(pattern="8..$", string=ex_loc)):
                    for loc_type in ["KW", "OW"]:
                        int_locs_select = [
                            int_loc for int_loc in int_locs if bool(re.match(pattern=f"{loc_type}.", string=int_loc))
                        ]
                        if len(np.unique([int_loc[:-1] for int_loc in int_locs_select])) > 1:
                            int_loc_error += list(int_locs_select)
                else:
                    int_loc_error = [
                        int_loc for int_loc in int_locs if not bool(re.match(pattern=f"...{ex_loc}..$", string=int_loc))
                    ]
            elif len(ex_loc) == 4:
                if bool(re.match(pattern=".8..$", string=ex_loc)):
                    for loc_type in ["KW", "OW"]:
                        int_locs_select = [
                            int_loc for int_loc in int_locs if bool(re.match(pattern=f"{loc_type}.", string=int_loc))
                        ]
                        if len(np.unique([int_loc[:-1] for int_loc in int_locs_select])) > 1:
                            int_loc_error += list(int_locs_select)
                else:
                    int_loc_error += [
                        int_loc for int_loc in int_locs if not bool(re.match(pattern=f"..{ex_loc}..$", string=int_loc))
                    ]

            assert self.ignored_ex_loc is not None, "this should not happen"
            if int(ex_loc) in self.ignored_ex_loc["externalLocation"].values:
                int_loc_error = [
                    int_loc
                    for int_loc in int_loc_error
                    if int_loc
                    not in self.ignored_ex_loc[self.ignored_ex_loc["externalLocation"] == int(ex_loc)][
                        "internalLocation"
                    ].values
                ]

            for int_loc in int_loc_error:
                ex_loc_errors["internalLocation"].append(int_loc)
                ex_loc_errors["externalLocation"].append(ex_loc)

        result_df = pd.DataFrame(data=ex_loc_errors)

        if len(result_df) == 0:
            logger.info("all external and internal locations consistent")
        else:
            logger.warning(f"{len(result_df)} external locations inconsistent with internal locations")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_timeseries_logic(self, sheet_name: str = "time_series error") -> ExcelSheet:
        """Check if timeseries are consistent with internal locations and parameters."""
        description = "tijdseries die niet logisch zijn gekoppeld aan interne locaties en parameters"
        logger.info(f"start {self.check_timeseries_logic.__name__} with sheet_name={sheet_name}")

        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)

        idmap_subloc_df = idmap_df[idmap_df["internalLocation"].isin(values=self.subloc.geo_df["LOC_ID"].values)]

        idmap_subloc_df["type"] = idmap_subloc_df["internalLocation"].apply(
            func=lambda x: self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == x]["TYPE"].values[0]
        )

        idmap_subloc_df["loc_group"] = idmap_subloc_df["internalLocation"].str[0:-1]

        ts_errors = {
            "internalLocation": [],
            "eind": [],
            "internalParameters": [],
            "externalParameters": [],
            "externalLocations": [],
            "error_type": [],
            "error": [],
        }

        for loc_group, group_df in idmap_subloc_df.groupby("loc_group"):
            ex_locs = np.unique(group_df["externalLocation"].values)
            ex_locs_dict = {ex_loc: idx for idx, ex_loc in enumerate(ex_locs)}
            split_ts = [
                key
                for key in ex_locs_dict.keys()
                if any([regex.match(string=key) for regex in [re.compile(pattern=rex) for rex in ["8..", ".8.."]]])
            ]

            ex_locs_skip = self.ignored_ts800[
                self.ignored_ts800["internalLocation"].isin(values=group_df["internalLocation"])
            ]["externalLocation"]

            split_ts = [key for key in split_ts if str(key) not in ex_locs_skip.values.astype(np.str)]

            ex_locs_dict = {
                k: (ex_locs_dict[k[1:]] if (k[1:] in ex_locs_dict.keys()) and (k not in split_ts) else v)
                for (k, v) in ex_locs_dict.items()
            }

            org_uniques = np.unique([val for key, val in ex_locs_dict.items() if key not in split_ts])
            if len(org_uniques) == 1 and len(split_ts) == 1:
                ex_locs_dict = {k: (org_uniques[0] if k in split_ts else v) for (k, v) in ex_locs_dict.items()}

            group_df["ex_loc_group"] = group_df["externalLocation"].apply(func=lambda x: ex_locs_dict[x])

            for int_loc, loc_df in group_df.groupby("internalLocation"):

                if int_loc in self.ignored_time_series_error["internalLocation"].values:
                    continue

                int_loc_df = self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == int_loc]
                sub_type = int_loc_df["TYPE"].values[0]
                startdate_str = int_loc_df["START"].values[0]
                enddate_str = int_loc_df["EIND"].values[0]

                if is_unmeasured_location(startdate=startdate_str, enddate=enddate_str):
                    continue

                end_time = pd.to_datetime(enddate_str)
                ex_pars = np.unique(loc_df["externalParameter"].values)
                int_pars = np.unique(loc_df["internalParameter"].values)
                ex_locs = np.unique(loc_df["externalLocation"].values)
                if sub_type in ["krooshek", "debietmeter"]:
                    # krooshek and debietmeter can not have stuurpeil ('HR.') as external parameter
                    if any([re.match(pattern="HR.", string=ex_par) for ex_par in ex_pars]):
                        ts_errors["internalLocation"].append(int_loc)
                        ts_errors["eind"].append(end_time)
                        ts_errors["internalParameters"].append(",".join(int_pars))
                        ts_errors["externalParameters"].append(",".join(ex_pars))
                        ts_errors["externalLocations"].append(",".join(ex_locs))
                        ts_errors["error_type"].append(sub_type)
                        ts_errors["error"].append(f"{sub_type} met stuurpeil")

                else:
                    if not any([re.match(pattern="HR.", string=ex_par) for ex_par in ex_pars]):
                        if any(
                            [
                                re.match(pattern="HR.", string=ex_par)
                                for ex_par in np.unique(group_df["externalParameter"])
                            ]
                        ):
                            if sub_type not in ["totaal", "vispassage"]:
                                if pd.Timestamp.now() < end_time:
                                    sp_locs = np.unique(
                                        group_df[group_df["externalParameter"].str.match("HR.")]["internalLocation"]
                                    )
                                    ts_errors["internalLocation"].append(int_loc)
                                    ts_errors["eind"].append(end_time)
                                    ts_errors["internalParameters"].append(",".join(int_pars))
                                    ts_errors["externalParameters"].append(",".join(ex_pars))
                                    ts_errors["externalLocations"].append(",".join(ex_locs))
                                    ts_errors["error_type"].append(sub_type)
                                    ts_errors["error"].append(f"{sub_type} zonder stuurpeil {','.join(sp_locs)} wel")
                    else:
                        time_series = loc_df.groupby(["ex_loc_group", "externalParameter"])
                        sp_series = [
                            series for series in time_series if bool(re.match(pattern="HR.", string=series[0][1]))
                        ]
                        for idx, series in enumerate(sp_series):
                            ex_par = series[0][1]
                            ex_locs = series[1]["externalLocation"]
                            int_par = np.unique(series[1]["internalParameter"])
                            if len(int_par) > 1:
                                ts_errors["internalLocation"].append(int_loc)
                                ts_errors["eind"].append(end_time)
                                ts_errors["internalParameters"].append(",".join(int_pars))
                                ts_errors["externalParameters"].append(",".join(ex_pars))
                                ts_errors["externalLocations"].append(",".join(ex_locs))
                                ts_errors["error_type"].append(sub_type)
                                error_msg = f'{",".join(int_par)} coupled to 1 sp-series (ex_par:{ex_par}, ex_loc(s):{",".join(ex_locs)})'  # noqa
                                ts_errors["error"].append(error_msg)
                            other_series = [series for idy, series in enumerate(sp_series) if idy != idx]

                            other_int_pars = [np.unique(series[1]["internalParameter"]) for series in other_series]

                            if len(other_int_pars) > 0:
                                other_int_pars = np.concatenate(other_int_pars)

                            conflicting_pars = [par for par in int_par if par in other_int_pars]

                            if len(conflicting_pars) > 0:
                                ts_errors["internalLocation"].append(int_loc)
                                ts_errors["eind"].append(end_time)
                                ts_errors["internalParameters"].append(",".join(int_pars))
                                ts_errors["externalParameters"].append(",".join(ex_pars))
                                ts_errors["externalLocations"].append(",".join(ex_locs))
                                ts_errors["error_type"].append(sub_type)
                                error_msg = f'{",".join(conflicting_pars)} coupled to sp-serie (ex_par:{ex_par}, ex_loc(s):{",".join(ex_locs)})'  # noqa
                                ts_errors["error"].append(error_msg)
        result_df = pd.DataFrame(data=ts_errors)
        if len(result_df) == 0:
            logger.info("logical coupling of all timeseries to internal locations/parameters")
        else:
            logger.warning(f"{len(result_df)} timeseries coupled illogical to internal locations/parameters")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_validation_rules(self, sheet_name: str = "validation error") -> ExcelSheet:
        """Check if validation rules are consistent.

        1. Per loc_set wordt er gelooped over de validatie csvs (df_merged_validation_csvs).
        2. Voor elke int_loc in csv wordt 0 of meerdere int_pars uit de IdOPVLWATER.xml gehaald
            - Bijv van 'KW101310' naar ['H.S.0', 'H2.S.0']
            - we doen bewust alleen IdOPVLWATER.xml want de validatie-CSV’s gelden alleen voor oppervlaktewater
              in het noneq-tijdperk na 2011, dus IdOPVLWATER.xml is toereikend.
        3. Als er 0 int_pars wordt gevonden dan naar skippen naar volgende regel in validatie csv
        4. Obv int_pars wordt dan de betreffende validatie_rules opgehaald:
            - all (voor hoofdloc) = ['HS1_HMAX', 'HS1_HMIN', 'HS2_HMAX', 'HS2_HMIN', 'HS3_HMAX', 'HS3_HMIN']
            - required = ['HS1_HMAX', 'HS1_HMIN', 'HS2_HMAX', 'HS2_HMIN']
            - verschil (all en required) = ['HS3_HMAX', 'HS3_HMIN']
        5. De validatie regel:
            - mag dan niet iets bevatten uit verschil
            - moet alles van required bevatten

        NOTE: validatie rules check voor par=Q.B (berekend debiet) wordt overgeslagen, want er zijn
        nog geen validatieregels voor Q.B
        """

        # TODO: validation_rule_check
        #  1) validatie perioden vandezelfde subloc mogen
        #       - niet overlappen
        #       - geen gaten
        #  2) constants.MIN_DATE_ALLOWED <= start < eind <= constants.MAX_DATE_ALLOWED

        # Roger 'algemeen validatie csvs'
        # Inloc in validatie-CSV’s
        # - Voor streefhoogte, hefhoogte, opening percentage hebben we aparte validatie csvs
        # - In Validatie csv staan validatie criteria per type tijdreeks
        # - Elke csv staat voor een type parameter
        # - Van een parameter zijn er meerdere locaties waar die voorkomt
        # - Per locatie (bijv KWxxxx) staat er een regel in zo'n csv:
        #     - Streef 1 H.S.0
        #     - streef 2 H2.S.0
        # - ff zij-stapje: alle validatie csvs kunnen meerdere validatie perioden hebben per kunstwerk:
        #     - 1 meetpunt kan meerdere validatie periode hebben
        #     - Locatie.csv heeft start end: zegt iets over geldigheid van de locatie
        #     - Oppvlwater_watervalidatie.csv heeft ook start- en endate: is start eind van validatie periode
        #     - Per definitie zijn deze validatie periode aansluitend (nooit een gat of overlappend!)
        #     - We hoeven deze Oppvlwater_watervalidatie.csv niet te relateren aan sublocaties (die hebben we nu ontkoppelt)  # noqa

        # Roger 'hoe validatie error regel oplossen?'
        # voorbeeld
        # internalLocation  start       eind        internalParameters  error_type  description
        # KW100412	        19960401    21000101    H.R.0,Hk.0,Q.G.0	too_few	    HR1_HMAX,HR1_HMIN

        # if error_type == 'value': daar is CAW verantwoordelijk voor (alle validatie instellingen).
        # if error_type == 'too_few' of 'too_many': wij eerst zelf actie ondernemen (zie hieronder):

        # 1. edit betreffende validatie csv:
        #       OW = MapLayerFiles/oppvlwater_watervalidatie.csv
        #       KW = MapLayerFiles/oppvlwater_kunstvalidatie_<type>.csv
        #   - HR1_MAX (voorbeeld hierboven) betreft dus stuurpeil1, dus pak oppvlwater_kunstvalidatie_stuur1.csv
        #   - KW nummer + start- + einddatum invullen
        #       start- en einddatum validatie csv is altijd 19000101 en 21000101, tenzij CAW validatie persoon
        #       vind dat ergens in de tijdreeks criteria in de tijd zijn veranderd: Dan maakt CAW een extra regel aan.
        #   - andere kolommen in validatie csv leeglaten
        # 2. wij maken mpt config klaar voor productie
        # 3. Job Verkaik upload de nieuwe kunstvalidatie csv in config middels de ConfiguratieManager
        #   - caw tijdreeksen worden van deze moment geimporteerd (niet met terugwerkende kracht)
        # 4. voor alle tijdreeksen die nog nooit zijn geimporteerd in WIS:
        #     - wij wij maken een extract van historie, die geven we aan Job Verkaik: "hier heb je 1 xml die al die
        #       historosiche data nog een keer bevat
        # 5. Nu kan CAW persoon pas fatsoenlijk validatie regels vastellen (want WIS bevat nu de gehele tijdreeks)
        #   - harde grenzen (bijv HMAX, HMIN):
        #       - voor met name water- en stuwstanden vastellen obv CAW sensorbereik onderstation van een kunstwerk.
        #       - voor streef en stuur: geen idee
        #   - zachte grenzen (bijv SMAX, SMIN):
        #       - vaststellen obv tijdreeks zelf
        # 6. WIS gebruikt deze bandbreedtes om tijdseries te vlaggen.

        description = "controle of attributen van validatieregels overbodig zijn/missen óf verkeerde waarden bevatten"
        logger.info(f"start {self.check_validation_rules.__name__} with sheet_name={sheet_name}")
        errors = {
            "internalLocation": [],
            "internalParameters": [],
            "start": [],
            "eind": [],
            "error_type": [],
            "error_description": [],
        }
        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)
        idmap_df_grouped_by_intloc = idmap_df.groupby("internalLocation")
        idmap_df[is_in_a_validation] = False

        for loc_set in (self.hoofdloc, self.subloc, self.waterstandloc, self.mswloc, self.psloc):
            if not loc_set.validation_rules:
                continue
            # merge all validation csv per loc_set
            df_merged_validation_csvs = HelperValidationRules.get_df_merged_validation_csvs(
                loc_set=loc_set, fews_config=self.fews_config
            )

            # keep track of idmapping int_locs that are in df_merged_validation_csvs
            mask = idmap_df["internalLocation"].isin(df_merged_validation_csvs["LOC_ID"])
            assert len(mask) == len(idmap_df)
            # update idmap_df[is_in_a_validation] to True when mask is True (never True to False!)
            idmap_df.loc[mask, is_in_a_validation] = True

            for idx, row in df_merged_validation_csvs.iterrows():
                # drop all empty columns current row so we can use row.keys() to check if value is missing
                row = row.dropna()
                # go from int_loc to 1 or more int_pars based on id_mapping
                # eg: from 'KW101310' to ['H.S.0', 'H2.S.0']
                int_pars = HelperValidationRules.get_int_pars(
                    idmap_df_grouped_by_intloc=idmap_df_grouped_by_intloc, int_loc=row["LOC_ID"]
                )
                if not int_pars:
                    logger.debug(f"no problem, int_loc {row['LOC_ID']} not in IdOPVLWATER")
                    continue
                errors = HelperValidationRules.check_attributes_too_few_or_many(
                    errors=errors,
                    loc_set=loc_set,
                    row=row,
                    int_pars=int_pars,
                )
                for validation_rule in loc_set.validation_rules:
                    matching_int_pars = [int_par.startswith(validation_rule["parameter"]) for int_par in int_pars]
                    if not any(matching_int_pars):
                        continue
                    rule = validation_rule["extreme_values"]
                    if loc_set in (self.hoofdloc, self.subloc):
                        errors = HelperValidationRules.check_hoofd_and_sub_loc(
                            errors=errors, rule=rule, row=row, int_pars=int_pars
                        )
                    elif loc_set == self.waterstandloc:
                        errors = HelperValidationRules.check_waterstandstand_loc(
                            errors=errors, rule=rule, row=row, int_pars=int_pars
                        )

        # TODO: remove this
        assert len(idmap_df[idmap_df[is_in_a_validation] == False])

        new_csv_creator = NewValidationCsvCreator(
            fews_config=self.fews_config,
            hoofdloc=self.hoofdloc,
            subloc=self.subloc,
            waterstandloc=self.waterstandloc,
            idmap_df=idmap_df,
        )
        self._validation_csvs_new = new_csv_creator.run()
        # bad design.. but new_csv_creator.idmap_df is updated in the meantime with two new columns
        idmap_df = new_csv_creator.idmap_df

        errors = HelperValidationRules.check_idmapping_int_loc_in_a_validation(errors=errors, idmap_df=idmap_df)

        result_df = pd.DataFrame(data=errors).drop_duplicates(keep="first", inplace=False)
        if len(result_df) == 0:
            logger.info("no missing incorrect validation rules")
        else:
            logger.warning(f"{len(result_df)} validation rules contain errors/are missing")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_int_par_ex_par_mismatch(self, sheet_name: str = "int_par ex_par mismatch") -> ExcelSheet:
        """Check if internal and external parameters are consistent."""
        description = "controle of externe parameters en interne parameters logisch aan elkaar gekoppeld zijn"
        logger.info(f"start {self.check_int_par_ex_par_mismatch.__name__} with sheet_name={sheet_name}")
        par_errors = {
            "internalLocation": [],
            "internalParameter": [],
            "externalParameter": [],
            "fout": [],
        }

        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)

        # about 12 OW locations have a ex_par 'H' (instead of 'H.B.x' or H.G.x').
        # roger: "Alle histtags horen altijd een volgnummer te hebben en HO of HB te zijn.
        # Ik verwacht niet dat we in de toekomst weer zo'n fout maken, dus een IGNORE-lijst zou hier
        # wellicht overdreven zijn en een uitzondering in de code een betere oplossing.
        whitelist_in_locs = [
            "OW263201",
            "OW263301",
            "OW263501",
            "OW363601",
            "OW363701",
            "OW462501",
            "OW462601",
            "OW462901",
            "OW463001",
            "OW463101",
            "OW463401",
            "OW462601",
        ]
        for idx, row in idmap_df.iterrows():
            in_par_row = row["internalParameter"]
            ex_par_row = row["externalParameter"]
            in_loc_row = row["internalLocation"]

            if in_loc_row in whitelist_in_locs and ex_par_row == "H":
                continue

            allowed_ex_pars = [
                mapping["external"]
                for mapping in constants.PARAMETER_MAPPING
                if re.match(pattern=f'{mapping["internal"]}[0-9]', string=in_par_row)
            ]

            error = None
            if not allowed_ex_pars:
                error = "in_par has no allowed ex_pars"
            else:
                if not any([re.match(pattern=par, string=ex_par_row) for par in allowed_ex_pars]):
                    error = "parameter mismatch"
            if not error:
                continue

            par_errors["internalLocation"].append(in_loc_row)
            par_errors["internalParameter"].append(in_par_row)
            par_errors["externalParameter"].append(ex_par_row)
            par_errors["fout"].append(error)

        result_df = pd.DataFrame(data=par_errors)

        if len(result_df) == 0:
            logger.info("no regex errors for internal and external parameters")
        else:
            logger.warning(f"{len(result_df)} regex errors for internal and external parameters")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_location_set_errors(self, sheet_name: str = "loc_set error") -> ExcelSheet:
        """Check on errors in locationsets."""
        description = (
            "controle of alle locatiesets logisch zijn opgebouwd, de juiste attribuut-verwijzingen"
            " hebben én consistent zijn per CAW-locatie"
        )
        logger.info(f"start {self.check_location_set_errors.__name__} with sheet_name={sheet_name}")

        loc_set_errors = {
            "locationId": [],
            "caw_code": [],
            "caw_name": [],
            "csv_file": [],
            "location_name": [],
            "type": [],
            "function": [],
            "name_error": [],
            "caw_name_inconsistent": [],
            "missing_in_map": [],
            "missing_in_set": [],
            "missing_peilschaal": [],
            "missing_hbov": [],
            "missing_hben": [],
            "missing_hbovps": [],
            "missing_hbenps": [],
            "missing_h_loc": [],
            "xy_not_same": [],
        }

        for loc_set in (self.hoofdloc, self.subloc, self.waterstandloc, self.mswloc, self.psloc):
            if loc_set.skip_check_location_set_error:
                continue
            int_locs = []
            for idmap in ["IdOPVLWATER", "IdOPVLWATER_HYMOS"]:
                section_start_end_list = constants.IDMAP_SECTIONS[idmap][loc_set.idmap_section_name]
                for section in section_start_end_list:
                    int_locs += [
                        item["internalLocation"]
                        for item in xml_to_dict(self.fews_config.IdMapFiles[idmap], **section)["idMap"]["map"]
                    ]

            if loc_set in (self.hoofdloc, self.subloc):
                int_locs = [loc for loc in int_locs if loc[-1] != "0"]

            for idx, row in list(loc_set.geo_df.iterrows()):
                error = {
                    "name_error": False,
                    "caw_name_inconsistent": False,
                    "missing_in_map": False,
                    "type": "",
                    "function": "",
                    "missing_in_set": False,
                    "missing_peilschaal": False,
                    "missing_hbov": False,
                    "missing_hben": False,
                    "missing_hbovps": False,
                    "missing_hbenps": False,
                    "missing_h_loc": False,
                    "xy_not_same": False,
                }

                loc_id = row["LOC_ID"]
                assert loc_id.startswith("OW") or loc_id.startswith(
                    "KW"
                ), f"expected loc_id {loc_id} to start with OW or KW "
                caw_code = loc_id[2:-2]
                assert caw_code.isdigit(), f"expected caw_code {caw_code} to be a digit"
                loc_name = row["LOC_NAME"]
                caw_name = ""

                if loc_set == self.subloc:

                    # TODO: moet dit wel hoofdlocaties zijn?
                    #  par_gdf = self.location_sets["hoofdlocaties"]["gdf"]
                    par_gdf = self.hoofdloc.geo_df
                    loc_function = row["FUNCTIE"]
                    sub_type = row["TYPE"]

                    if sub_type in [
                        "afsluiter",
                        "debietmeter",
                        "krooshek",
                        "vispassage",
                    ]:
                        if not re.match(pattern=f"[A-Z0-9 ]*_{caw_code}-K_[A-Z0-9 ]*-{sub_type}", string=loc_name):
                            error["name_error"] = True

                    else:
                        if not re.match(
                            pattern=f"[A-Z0-9 ]*_{caw_code}-K_[A-Z0-9 ]*-{sub_type}[0-9]_{loc_function}",
                            string=loc_name,
                        ):
                            error["name_error"] = True

                    if not error["name_error"]:
                        caw_name = re.match(pattern="([A-Z0-9 ]*)_", string=loc_name).group(1)
                        if not all(
                            loc_set.geo_df[loc_set.geo_df["LOC_ID"].str.match(f"..{caw_code}")]["LOC_NAME"].str.match(
                                f"({caw_name}_{caw_code}-K)"
                            )
                        ):
                            error["caw_name_inconsistent"] = True

                    if row["HBOV"] not in self.waterstandloc.geo_df["LOC_ID"].values:
                        error["missing_hbov"] = True

                    if row["HBEN"] not in self.waterstandloc.geo_df["LOC_ID"].values:
                        error["missing_hben"] = True

                    if row["HBOVPS"] not in self.psloc.geo_df["LOC_ID"].values:
                        error["missing_hbovps"] = True

                    if row["HBENPS"] not in self.psloc.geo_df["LOC_ID"].values:
                        error["missing_hbenps"] = True

                    if row["PAR_ID"] not in self.hoofdloc.geo_df["LOC_ID"].values:
                        error["missing_h_loc"] = True

                    else:
                        if not any(
                            [re.match(pattern=loc, string=loc_id) for loc in self.ignored_xy["internalLocation"]]
                        ):
                            par_gdf_row = par_gdf[par_gdf["LOC_ID"] == row["PAR_ID"]]
                            par_gdf_geom = par_gdf_row["geometry"].values[0]
                            if not par_gdf_geom.equals(row["geometry"]):
                                error["xy_not_same"] = True

                    if any(error.values()):
                        error["type"] = sub_type
                        error["function"] = loc_function

                elif loc_set == self.hoofdloc:
                    if not re.match(pattern=f"[A-Z0-9 ]*_{caw_code}-K_[A-Z0-9 ]*", string=loc_name):
                        error["name_error"] = True

                elif loc_set == self.waterstandloc:
                    if not re.match(pattern=f"[A-Z0-9 ]*_{caw_code}-w_.*", string=loc_name):
                        error["name_error"] = True

                    if not error["name_error"]:
                        caw_name = re.match(pattern="([A-Z0-9 ]*)_", string=loc_name).group(1)
                        if not all(
                            loc_set.geo_df[loc_set.geo_df["LOC_ID"].str.match(f"..{caw_code}")]["LOC_NAME"].str.match(
                                f"({caw_name}_{caw_code}-w)"
                            )
                        ):
                            error["caw_name_inconsistent"] = True

                    if row["PEILSCHAAL"] not in self.psloc.geo_df["LOC_ID"].values:
                        error["missing_peilschaal"] = True

                    if loc_id not in int_locs:
                        error["missing_in_map"] = True

                if any(error.values()):
                    loc_set_errors["locationId"].append(loc_id)
                    loc_set_errors["caw_name"].append(caw_name)
                    loc_set_errors["caw_code"].append(caw_code)
                    loc_set_errors["csv_file"].append(loc_set.csv_filename)
                    loc_set_errors["location_name"].append(loc_name)
                    for key, value in error.items():
                        loc_set_errors[key].append(value)

        result_df = pd.DataFrame(data=loc_set_errors)
        if len(result_df) == 0:
            logger.info("no errors in locationSets")
        else:
            logger.warning(f"{len(result_df)} errors in locationSets")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def _add_input_files_to_results(self) -> None:
        """each input files is a excel sheet with type is input, as opposeded to check results results which are
        excel sheets with type is output."""
        self.results.add_sheet(
            excelsheet=ExcelSheet(
                name="ignored_ex_loc",
                description=constants.PathConstants.ignored_ex_loc.value.description,
                df=self.ignored_ex_loc,
                sheet_type=ExcelSheetTypeChoices.input,
            )
        )
        self.results.add_sheet(
            excelsheet=ExcelSheet(
                name="ignored_histtag",
                description=constants.PathConstants.ignored_histtag.value.description,
                df=self.ignored_histtag,
                sheet_type=ExcelSheetTypeChoices.input,
            )
        )
        self.results.add_sheet(
            excelsheet=ExcelSheet(
                name="ignored_ts800",
                description=constants.PathConstants.ignored_ts800.value.description,
                df=self.ignored_ts800,
                sheet_type=ExcelSheetTypeChoices.input,
            )
        )
        self.results.add_sheet(
            excelsheet=ExcelSheet(
                name="ignored_xy",
                description=constants.PathConstants.ignored_xy.value.description,
                df=self.ignored_xy,
                sheet_type=ExcelSheetTypeChoices.input,
            )
        )

    def _add_paths_to_results(self) -> None:
        columns = ["name", "path", "description"]
        data = [
            (path_constant.name, path_constant.value.path.as_posix(), path_constant.value.description)
            for path_constant in constants.PathConstants
        ]
        path_df = pd.DataFrame(data=data, columns=columns)
        excelsheet = ExcelSheet(
            name="used_paths",
            df=path_df,
            description="beschrijving van en absoluut pad naar gebruikte bestanden",
            sheet_type=ExcelSheetTypeChoices.output_no_check,
        )
        self.results.add_sheet(excelsheet=excelsheet)

    def _add_tab_color_description_to_results(self):
        data = ExcelSheetTypeChoices.tab_color_description()
        columns = ["description", "color"]
        description_df = pd.DataFrame(data=data, columns=columns)
        excelsheet = ExcelSheet(
            name="tab_colors",
            df=description_df,
            description="beschrijving van tabblad kleuren",
            sheet_type=ExcelSheetTypeChoices.output_no_check,
        )
        self.results.add_sheet(excelsheet=excelsheet)

    def _add_mpt_histtags_new_to_results(self):
        excelsheet = ExcelSheet(
            name="mpt_histtags_new",
            df=self.mpt_histtags_new,
            description="alle meetpunt ids uitgelezen uit de histTags.csv, die niet in de ignore "
            "staan en in de idmapping zijn opgenomen",
            sheet_type=ExcelSheetTypeChoices.output_no_check,
        )
        self.results.add_sheet(excelsheet=excelsheet)

    def run(self):
        # self.results.add_sheet(excelsheet=self.check_idmap_int_loc_in_csv())
        # self.results.add_sheet(excelsheet=self.check_dates_loc_sets())
        # self.results.add_sheet(excelsheet=self.check_idmap_sections())
        # self.results.add_sheet(excelsheet=self.check_ignored_histtags())
        # self.results.add_sheet(excelsheet=self.check_histtags_nomatch())
        # self.results.add_sheet(excelsheet=self.check_double_idmaps())
        # self.results.add_sheet(excelsheet=self.check_missing_pars())
        # self.results.add_sheet(excelsheet=self.check_s_loc_consistency())
        #
        # # check returns two results
        # sheet1, sheet2 = self.check_ex_par_errors_int_loc_missing()
        # self.results.add_sheet(excelsheet=sheet1)
        # self.results.add_sheet(excelsheet=sheet2)
        #
        # self.results.add_sheet(excelsheet=self.check_ex_par_missing())
        # self.results.add_sheet(excelsheet=self.check_ex_loc_int_loc_mismatch())
        # self.results.add_sheet(excelsheet=self.check_timeseries_logic())
        self.results.add_sheet(excelsheet=self.check_validation_rules())
        # self.results.add_sheet(excelsheet=self.check_int_par_ex_par_mismatch())
        # self.results.add_sheet(excelsheet=self.check_location_set_errors())

        # add output_no_check sheets
        self._add_tab_color_description_to_results()
        self._add_paths_to_results()
        self._add_input_files_to_results()
        self._add_mpt_histtags_new_to_results()

        # write excel file with check results
        excel_writer = ExcelWriter(results=self.results)
        excel_writer.write()

        # write new csv files
        # self._write_new_opvlwater_hoofdloc_csv()
        # self._write_new_opvlwater_subloc_csv()
        # self._write_new_waterstandlocaties_csv()
        self._write_new_validation_csvs()
