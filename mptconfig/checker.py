from mptconfig import constants
from mptconfig.excel import ExcelSheet
from mptconfig.excel import ExcelSheetCollector
from mptconfig.excel import ExcelSheetTypeChoices
from mptconfig.excel import ExcelWriter
from mptconfig.fews_utilities import FewsConfig
from mptconfig.fews_utilities import xml_to_dict
from mptconfig.tmp import validate_expected_summary
from mptconfig.utils import flatten_nested_list
from mptconfig.utils import idmap2tags
from mptconfig.utils import sort_validation_attribs
from mptconfig.utils import update_date
from mptconfig.utils import update_h_locs
from mptconfig.utils import update_histtag
from pathlib import Path
from shapely.geometry import Point  # noqa shapely comes with geopandas
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

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
        self._updated_opvlwater_hoofdloc = None
        self._hoofdloc = None
        self._hoofdloc_new_geo_df = None
        self._subloc = None
        self._waterstandloc = None
        self._mswloc = None
        self._psloc = None
        self._mpt_histtags = None
        self._mpt_histtags_new = None
        self._fews_config = None
        self._ignored_ex_loc = None
        self._ignored_histtag = None
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
        self._histtags = pd.read_csv(
            filepath_or_buffer=constants.PathConstants.histtags_csv.value.path,
            parse_dates=dtype_columns,
            sep=None,
            engine="python",
        )
        for dtype_column in dtype_columns:
            if not pd.api.types.is_datetime64_dtype(self.histtags[dtype_column]):
                raise AssertionError(
                    f"dtype_column {dtype_column} in {constants.PathConstants.histtags_csv.value.path} "
                    f"can not be converted to np.datetime64. Check if values are dates."
                )
        return self._histtags

    @property
    def hoofdloc(self) -> constants.LocationSet:
        """Get the latest version of the hoofdlocation: hoofdloc_new or else hoofdloc"""
        if self._hoofdloc_new_geo_df is not None:
            assert self._hoofdloc and isinstance(self._hoofdloc, constants.LocationSet)
            assert isinstance(self._hoofdloc_new_geo_df, pd.DataFrame)
            self._hoofdloc._geo_df = self._hoofdloc_new_geo_df
        if self._hoofdloc is not None:
            return self._hoofdloc
        self._hoofdloc = constants.HoofdLocationSet(fews_config=self.fews_config)
        return self._hoofdloc

    @property
    def hoofdloc_new_geo_df(self) -> Optional[pd.DataFrame]:
        return self._hoofdloc_new_geo_df

    @property
    def subloc(self) -> constants.LocationSet:
        if self._subloc is not None:
            return self._subloc
        self._subloc = constants.SubLocationSet(fews_config=self.fews_config)
        return self._subloc

    @property
    def waterstandloc(self) -> constants.LocationSet:
        if self._waterstandloc is not None:
            return self._waterstandloc
        self._waterstandloc = constants.WaterstandLocationSet(fews_config=self.fews_config)
        return self._waterstandloc

    @property
    def mswloc(self) -> constants.LocationSet:
        if self._mswloc is not None:
            return self._mswloc
        self._mswloc = constants.MswLocationSet(fews_config=self.fews_config)
        return self._mswloc

    @property
    def psloc(self) -> constants.LocationSet:
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
        in de ignore staan en in de idmapping zijn opgenomen."""
        # TODO: ask Roger what is the purpose of this selection? and why is it in excel output
        #  file (as separate tab 'mpt_histtags_new')?.
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
            columns={"fews_locid": "LOC_ID", "total_min_start_dt": "STARTDATE", "total_max_end_dt": "ENDDATE"},
            inplace=True,
        )
        kw_locs = list(mpt_df[mpt_df["LOC_ID"].str.startswith("KW")]["LOC_ID"])
        # H_LOC ends with a 0 (e.g if subloc = KW106013, then h_loc becomes KW106010)
        h_locs = np.unique([f"{kw_loc[0:-1]}0" for kw_loc in kw_locs])
        h_locs_missing = [loc for loc in h_locs if loc not in mpt_df["LOC_ID"].to_list()]
        h_locs_df = pd.DataFrame(
            data={
                "LOC_ID": h_locs_missing,
                "STARTDATE": [pd.NaT] * len(h_locs_missing),
                "ENDDATE": [pd.NaT] * len(h_locs_missing),
            }
        )
        mpt_df = pd.concat([mpt_df, h_locs_df], axis=0)
        assert mpt_df["LOC_ID"].is_unique, "LOC_ID must be unique after pd.concat"
        mpt_df[["STARTDATE", "ENDDATE"]] = mpt_df.apply(
            func=update_h_locs, args=[h_locs, mpt_df], axis=1, result_type="expand"
        )
        assert mpt_df["LOC_ID"].is_unique, "LOC_ID must be unique after update_h_locs"
        assert not mpt_df["STARTDATE"].hasnans, "mpt_df column STARTDATE should not have nans"
        assert not mpt_df["ENDDATE"].hasnans, "mpt_df column ENDDATE should not have nans"
        self._mpt_histtags_new = mpt_df.sort_values(by="LOC_ID", ascending=True, ignore_index=True, inplace=False)
        assert sorted(self._mpt_histtags_new.columns) == ["ENDDATE", "LOC_ID", "STARTDATE"]
        return self._mpt_histtags_new

    @property
    def ignored_ex_loc(self) -> pd.DataFrame:
        if self._ignored_ex_loc is not None:
            return self._ignored_ex_loc
        logger.info(f"reading {constants.PathConstants.ignored_ex_loc.value.path}")
        self._ignored_ex_loc = pd.read_csv(
            filepath_or_buffer=constants.PathConstants.ignored_ex_loc.value.path,
            sep=",",
            engine="python",
        )
        assert sorted(self._ignored_ex_loc.columns) == ["externalLocation", "internalLocation"]
        return self._ignored_ex_loc

    @property
    def ignored_histtag(self) -> pd.DataFrame:
        if self._ignored_histtag is not None:
            return self._ignored_histtag
        logger.info(f"reading {constants.PathConstants.ignored_histtag.value.path}")
        self._ignored_histtag = pd.read_csv(
            filepath_or_buffer=constants.PathConstants.ignored_histtag.value.path,
            sep=",",
            engine="python",
        )
        assert sorted(self._ignored_histtag.columns) == ["ENDDATE", "STARTDATE", "UNKNOWN_SERIE"]
        self._ignored_histtag["UNKNOWN_SERIE"] = self._ignored_histtag["UNKNOWN_SERIE"].str.replace("#", "")
        return self._ignored_histtag

    @property
    def ignored_ts800(self) -> pd.DataFrame:
        if self._ignored_ts800 is not None:
            return self._ignored_ts800
        logger.info(f"reading {constants.PathConstants.ignored_ts800.value.path}")
        self._ignored_ts800 = pd.read_csv(
            filepath_or_buffer=constants.PathConstants.ignored_ts800.value.path,
            sep=",",
            engine="python",
        )
        assert sorted(self._ignored_ts800.columns) == ["externalLocation", "internalLocation"]
        return self._ignored_ts800

    @property
    def ignored_xy(self) -> pd.DataFrame:
        if self._ignored_xy is not None:
            return self._ignored_xy
        logger.info(f"reading {constants.PathConstants.ignored_xy.value.path}")
        self._ignored_xy = pd.read_csv(
            filepath_or_buffer=constants.PathConstants.ignored_xy.value.path,
            sep=",",
            engine="python",
        )
        assert sorted(self._ignored_xy.columns) == ["internalLocation", "x", "y"]
        return self._ignored_xy

    def _update_start_end_new_csv(self, location_set: constants.LocationSet) -> pd.DataFrame:
        assert isinstance(location_set, constants.LocationSet), f"location_set {location_set} is not a LocationSet"
        date_threshold = self.mpt_histtags_new["ENDDATE"].max() - pd.Timedelta(weeks=26)
        gdf = location_set.geo_df
        df = gdf.drop("geometry", axis=1)
        df[["START", "EIND"]] = df.apply(
            func=update_date, args=(self.mpt_histtags_new, date_threshold), axis=1, result_type="expand"
        )
        return df

    @staticmethod
    def df_to_csv(df: pd.DataFrame, file_name: str) -> None:
        csv_file_path = constants.PathConstants.output_dir.value.path / file_name
        if csv_file_path.suffix == "":
            csv_file_path = Path(f"{csv_file_path}.csv")
        if csv_file_path.is_file():
            f"overwriting existing file with path {csv_file_path}"
        df.to_csv(path_or_buf=csv_file_path.as_posix(), index=False)
        logger.debug(f"created {file_name}")

    def create_opvlwater_hoofdloc_csv_new(self) -> None:
        logger.info(f"creating new csv {self.hoofdloc.name}")
        df = self._update_start_end_new_csv(location_set=self.hoofdloc)
        # get existing fews config file name
        self.df_to_csv(df=df, file_name=self.hoofdloc.name)

    def create_opvlwater_subloc_csv_new(self) -> None:
        logger.info(f"creating new csv {self.subloc.name}")
        df = self._update_start_end_new_csv(location_set=self.subloc)
        grouper = df.groupby(["PAR_ID"])
        par_types_df = grouper["TYPE"].unique().apply(func=lambda x: sorted(x)).transform(lambda x: "/".join(x))
        # TODO: uitzoeken, gaat dit wel helemaal goed? want het was eerst
        #  df["PAR_ID"] = gdf["LOC_ID"].str[0:-1] + "0" (die gdf in _update_start_end_new_csv)
        df["PAR_ID"] = df["LOC_ID"].str[0:-1] + "0"
        df["ALLE_TYPES"] = df["PAR_ID"].apply(func=lambda x: par_types_df.loc[x])
        df[["HBOVPS", "HBENPS"]] = df.apply(func=self._update_staff_gauge, axis=1, result_type="expand")
        # get existing fews config file name
        self.df_to_csv(df=df, file_name=self.subloc.name)

    def create_waterstandlocaties_csv_new(self) -> None:
        logger.info(f"creating new csv {self.waterstandloc.name}")
        df = self._update_start_end_new_csv(location_set=self.waterstandloc)
        grouper = self.mpt_histtags.groupby(["fews_locid"])
        # leave it HIST_TAG (instead of HISTTAG), as that is what OPVLWATER_WATERSTANDEN_AUTO.csv expects
        df["HIST_TAG"] = df.apply(func=update_histtag, args=[grouper], axis=1, result_type="expand")
        self.df_to_csv(df=df, file_name=self.waterstandloc.name)

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

    def _create_hoofdloc_new_geo_df(self, par_dict: Dict) -> None:
        """Create a new hoofdloc from sublocs in case no errors found during
        check_h_loc_consistency in case all sublocs of same h_loc have consistent parameters."""
        # TODO: what is diff between hoofdloc_new and updated_opvlwater_hoofdloc??
        assert isinstance(par_dict, dict), f"par_dict should be a dictionary, not a {type(par_dict)}"
        par_gdf = pd.DataFrame(data=par_dict)
        columns = list(self.hoofdloc.geo_df.columns)
        drop_cols = [col for col in columns if col in par_gdf.columns and col != "LOC_ID"]
        drop_cols = drop_cols + ["geometry"]
        new_geo_df = self.hoofdloc.geo_df.drop(drop_cols, axis=1, inplace=False)
        new_geo_df = par_gdf.merge(new_geo_df, on="LOC_ID")
        new_geo_df["geometry"] = new_geo_df.apply(func=(lambda x: Point(float(x["X"]), float(x["Y"]))), axis=1)
        new_geo_df = new_geo_df[columns]
        self._hoofdloc_new_geo_df = new_geo_df

    def _update_staff_gauge(self, row: pd.Series) -> Tuple[str, str]:
        """Assign upstream and downstream staff gauges to subloc."""
        result = {"HBOV": "", "HBEN": ""}
        for key in result.keys():
            df = self.waterstandloc.geo_df.loc[self.waterstandloc.geo_df["LOC_ID"] == row[key]]
            if not df.empty:
                result[key] = df["PEILSCHAAL"].values[0]
        return result["HBOV"], result["HBEN"]

    def check_idmap_sections(self, sheet_name: str = "idmap section error") -> ExcelSheet:
        """Check if all KW/OW locations are in the correct section."""
        description = "Idmaps die niet in de juiste sectie zijn opgenomen"
        logger.info(f"start {self.check_idmap_sections.__name__}")
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
        logger.info(f"start {self.check_ignored_histtags.__name__}")
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
        if not result_df.empty:
            logger.warning(f"{len(result_df)} histTags should not be in ignored histtags")
        else:
            logger.info("hisTags ignore list consistent with idmaps")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_histtags_nomatch(self, sheet_name: str = "histtags nomatch") -> ExcelSheet:
        """Check if hisTags can be mapped to internal location (if there are not included in histtag_ignore list)"""
        description = (
            "hisTags die niet konden worden gemapped naar interne locatie en niet in de hisTag_ignore zijn opgenomen"
        )
        logger.info(f"start double{self.check_histtags_nomatch.__name__}")
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
        if not result_df.empty:
            logger.warning(f"{len(result_df)} histTags not in idMaps")
        else:
            logger.info("all histTags in idMaps")
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
        logger.info(f"start {self.check_double_idmaps.__name__}")
        result_df = pd.DataFrame(
            columns=["bestand", "externalLocation", "externalParameter", "internalLocation", "internalParameter"]
        )
        for idmap_file in constants.IDMAP_FILES:
            idmaps = self._get_idmaps(idmap_files=[idmap_file])
            idmap_doubles = [idmap for idmap in idmaps if idmaps.count(idmap) > 1]
            if not idmap_doubles:
                logger.info(f"No double idmaps in {idmap_file}")
                continue
            idmap_doubles = list({idmap["externalLocation"]: idmap for idmap in idmap_doubles}.values())
            logger.warning(f"{len(idmap_doubles)} double idmaps in {idmap_file}")
            df = pd.DataFrame(
                data=idmap_doubles,
                columns=["internalLocation", "externalLocation", "internalParameter", "externalParameter"],
            )
            df["bestand"] = idmap_file
            result_df = pd.concat(objs=[result_df, df], axis=0, join="outer")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_missing_pars(self, sheet_name: str = "pars missing") -> ExcelSheet:
        """Check if internal parameters in idmaps are missing in parameters.xml.
        All id_mapping.xml inpars (e.g. ‘H.R.0’) must exists in RegionConfigFiles/parameters.xml"""
        description = "controle of interne parameters missen in paramters.xml"
        logger.info(f"start {self.check_missing_pars.__name__}")
        config_parameters = list(self.fews_config.get_parameters(dict_keys="parameters").keys())

        idmaps = self._get_idmaps()
        id_map_parameters = [id_map["internalParameter"] for id_map in idmaps]
        params_missing = [parameter for parameter in id_map_parameters if parameter not in config_parameters]

        if len(params_missing) == 0:
            logger.info("all internal paramters are in config")
        else:
            logger.warning(f"{len(params_missing)} parameter(s) in idMaps are missing in config")
        result_df = pd.DataFrame(data={"parameters": params_missing})
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_h_loc(self, sheet_name: str = "h_loc error") -> ExcelSheet:
        """Check if all sub_locs of the same h_loc have consistent parameters: xy, rayon, systeem, kompas."""
        description = "fouten in CAW sublocatie-groepen waardoor hier geen hoofdlocaties.csv uit kan worden geschreven"
        logger.info(f"start {self.check_h_loc.__name__}")

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

            if len(loc_names) != 1:
                errors["LOC_NAME"] = ",".join(loc_names)
            else:
                fields["LOC_NAME"] = loc_names[0]

            if any([re.match(pattern=loc, string=loc_id) for loc in self.ignored_xy["internalLocation"]]):
                fields["X"], fields["Y"] = next(
                    [row["x"], row["y"]]
                    for index, row in self.ignored_xy.iterrows()
                    if re.match(pattern=row["internalLocation"], string=loc_id)
                )

            else:
                geoms = gdf["geometry"].unique()
                if len(geoms) != 1:
                    errors["GEOMETRY"] = ",".join([f"({geom.x} {geom.y})" for geom in geoms])
                else:
                    fields["X"] = geoms[0].x
                    fields["Y"] = geoms[0].y

            all_types = list(gdf["TYPE"].unique())
            all_types.sort()
            fields["ALLE_TYPES"] = "/".join(all_types)
            fields["START"] = gdf["START"].min()
            fields["EIND"] = gdf["EIND"].max()
            for attribuut in ["SYSTEEM", "RAYON", "KOMPAS"]:
                vals = gdf[attribuut].unique()
                if len(vals) != 1:
                    errors[attribuut] = ",".join(vals)
                else:
                    fields[attribuut] = vals[0]
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
        nr_errors_found = len(result_df)
        if nr_errors_found:
            logger.warning(f"{nr_errors_found} errors in consistency h_locs")
            logger.warning("h_locs will only be re-written when consistency errors are resolved")
        else:
            logger.info("no consistency errors. Rewrite h_locs from sublocs")
            self._create_hoofdloc_new_geo_df(par_dict=par_dict)
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

        logger.info(f"start {self.check_ex_par_errors_int_loc_missing.__name__}")

        ex_par_errors = {
            "internalLocation": [],  # TODO: can this be changed to int_loc, of flikkeren er dan weer dingen om..
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
        # niet veranderen, maar wel sidenote bij intepreter van result_df:
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

        # TODO: wat nu elke keer terug (7 locaties) komt moeten we wel gaan ignoren.
        #  Want Inke moet dat gaan uitzoeken en het is moeilijk om dit te onthouden
        #  ik heb nu een ignored_time_series_error.csv toegevoegd met die 7 locaties:
        #  1. verifieer of die 7 kloppen (obv historische mailwisseling met Inke <--> Roger/Renier)
        #  2. verwijs hier naar die nieuwe ignored lijst (en skip die locaties)

        description = "locaties waar externe parameters missen"
        logger.info(f"start {self.check_ex_par_missing.__name__}")
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

            loc_group = next(
                (df for loc, df in idmap_df.groupby("internalLocation") if loc == int_loc),
                pd.DataFrame(),
            )

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

    def check_ex_loc_int_loc(self, sheet_name: str = "ex_loc error") -> ExcelSheet:
        """Check if external locations are consistent with internal locations."""
        description = "externe locaties die niet passen bij interne locatie"
        logger.info(f"start {self.check_ex_loc_int_loc.__name__}")
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

            # TODO: @renier: what is backup if no self.ignored_ex_loc?
            assert self.ignored_ex_loc is not None
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
        logger.info(f"start {self.check_timeseries_logic.__name__}")

        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)

        idmap_subloc_df = idmap_df[idmap_df["internalLocation"].isin(values=self.subloc.geo_df["LOC_ID"].values)]

        idmap_subloc_df["type"] = idmap_subloc_df["internalLocation"].apply(
            func=(lambda x: self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == x]["TYPE"].values[0])
        )

        idmap_subloc_df["loc_group"] = idmap_subloc_df["internalLocation"].str[0:-1]

        ts_errors = {
            "internalLocation": [],
            "eind": [],
            "internalParameters": [],
            "externalParameters": [],
            "externalLocations": [],
            "type": [],
            "fout": [],
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

            group_df["ex_loc_group"] = group_df["externalLocation"].apply(func=(lambda x: ex_locs_dict[x]))

            for int_loc, loc_df in group_df.groupby("internalLocation"):
                sub_type = self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == int_loc]["TYPE"].values[0]
                date_str = self.subloc.geo_df[self.subloc.geo_df["LOC_ID"] == int_loc]["EIND"].values[0]
                try:
                    end_time = pd.to_datetime(date_str)
                except pd.errors.OutOfBoundsDatetime as err:
                    # TODO: 32101230 is een fictieve datum voor onbemeten locaties
                    #  pandas kan dat niet converteren naar datum, want:
                    #  Timestamp.max = Timestamp('2262-04-11 23:47:16.854775807')
                    #  maw: wellicht niet 32101230 gebruiken, maar 22220101
                    #  sowieso ergens definieren wat 19000101, 21000101, en 22220101 zijn
                    logger.warning(
                        f"fffffffffffffiiiiiiiiiiiiiiiixxxxx this: subloc contains out of bound "
                        f"date '{date_str}' cannot be converted, err={err}"
                    )
                ex_pars = np.unique(loc_df["externalParameter"].values)
                int_pars = np.unique(loc_df["internalParameter"].values)
                ex_locs = np.unique(loc_df["externalLocation"].values)
                if sub_type in ["krooshek", "debietmeter"]:
                    if any([re.match(pattern="HR.", string=ex_par) for ex_par in ex_pars]):
                        ts_errors["internalLocation"].append(int_loc)
                        ts_errors["eind"].append(end_time)
                        ts_errors["internalParameters"].append(",".join(int_pars))
                        ts_errors["externalParameters"].append(",".join(ex_pars))
                        ts_errors["externalLocations"].append(",".join(ex_locs))
                        ts_errors["type"].append(sub_type)
                        ts_errors["fout"].append(f"{sub_type} met stuurpeil")

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
                                    ts_errors["type"].append(sub_type)
                                    ts_errors["fout"].append(f"{sub_type} zonder stuurpeil {','.join(sp_locs)} wel")
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
                                ts_errors["type"].append(sub_type)
                                fout_msg = f'{",".join(int_par)} coupled to 1 sp-series (ex_par:{ex_par}, ex_loc(s):{",".join(ex_locs)})'  # noqa
                                ts_errors["fout"].append(fout_msg)
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
                                ts_errors["type"].append(sub_type)
                                fout_msg = f'{",".join(conflicting_pars)} coupled to sp-serie (ex_par:{ex_par}, ex_loc(s):{",".join(ex_locs)})'  # noqa
                                ts_errors["fout"].append(fout_msg)
        result_df = pd.DataFrame(data=ts_errors)
        if len(result_df) == 0:
            logger.info("logical coupling of all timeseries to internal locations/parameters")
        else:
            logger.warning(f"{len(result_df)} timeseries coupled illogical to internal locations/parameters")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def __create_location_set_df(self, loc_set: constants.LocationSet) -> pd.DataFrame:
        assert isinstance(loc_set, constants.LocationSet)
        location_set_df = loc_set.geo_df

        for attrib_file in loc_set.attrib_files:

            attribs = attrib_file["attribute"]
            if not isinstance(attrib_file["attribute"], list):
                attribs = [attribs]
            attribs = [attrib["number"].replace("%", "") for attrib in attribs if "number" in attrib.keys()]
            # watch out: attrib_file_name != loc_set.value.csvfile !!!
            attrib_file_name = Path(attrib_file["csvFile"]).stem
            csv_file_path = self.fews_config.MapLayerFiles[attrib_file_name]
            attrib_df = pd.read_csv(
                filepath_or_buffer=csv_file_path,
                sep=None,
                engine="python",
            )
            join_id = attrib_file["id"].replace("%", "")
            attrib_df.rename(columns={join_id: "LOC_ID"}, inplace=True)

            # TODO: ask roger which validation csvs must have unique LOC_ID? No csv at all right?
            #  Moreover, unique_together is {LOC_ID, STARTDATE, ENDDATE} right?
            # if not attrib_df["LOC_ID"].is_unique:
            #     logger.warning(f"LOC_ID is not unique in {attrib_file_name}")
            # TODO: check dates somewhere else (separate check?): validation_rules may eg not overlap (1 KW can have
            #  >1 validation_rule with own period.
            assert "END" not in attrib_df.columns, f"expected EIND, not END... {csv_file_path}"
            if ("START" and "EIND") in attrib_df.columns:
                not_okay = attrib_df[pd.to_datetime(attrib_df["EIND"]) <= pd.to_datetime(attrib_df["START"])]
                assert len(not_okay) == 0, f"EIND must be > START, {len(not_okay)} wrong rows in {attrib_file_name}"

            drop_cols = [col for col in attrib_df if col not in attribs + ["LOC_ID"]]
            attrib_df.drop(columns=drop_cols, axis=1, inplace=True)
            location_set_df = location_set_df.merge(attrib_df, on="LOC_ID", how="outer")
        return location_set_df

    def check_validation_rules(self, sheet_name: str = "validation error") -> ExcelSheet:
        """Check if validation rules are consistent."""
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
        #     - Oppvlwater_watervalidatie.csv heeft ook start endate: is start eind van validatie periode
        #     - Per definitie zijn deze validatie periode aansluitend (nooit een gat of overlappend!)
        #     - We hoeven deze Oppvlwater_watervalidatie.csv niet te relateren aan sublocaties (die hebben we nu ontkoppelt)  # noqa

        # Roger 'hoe validatie error regel oplossen?'
        # ps: Inke Leunk (hieronder genoemd) = tijdreeks validatie persoon van CAW
        # "internalLocation  "start":  "eind":      "internalParameters":  "fout_type": [] fout_beschrijving
        # KW100412	        19960401	21000101	H.R.0,Hk.0,Q.G.0	    missend	        HR1_HMAX,HR1_HMIN

        # if fout_type == 'waarde': daar is Inke verantwoordleijk voor (alle validatie instellingen).
        # if fout_type == 'missend' of 'overbodig': wij eerst zelf actie ondernemen (zie hieronder):

        # 1. edit betreffende validatie csv:
        #       OW = MapLayerFiles/oppvlwater_watervalidatie.csv
        #       KW = MapLayerFiles/oppvlwater_kunstvalidatie_<type>.csv
        #   - HR1_MAX (voorbeeld hierboven) betreft dus stuurpeil1, dus pak oppvlwater_kunstvalidatie_stuur1.csv
        #   - KW nummer + start- + einddatum invullen
        #       start- en einddatum validatie csv is altijd 19000101 en 21000101, tenzij CAW validatie persoon (Inke)
        #       vind dat ergens in de tijdreeks criteria in de tijd zijn veranderd: Dan maakt Inke een extra regel aan.
        #   - andere kolommen in validatie csv leeglaten
        # 2. wij maken mpt config klaar voor productie
        # 3. Job Verkaik upload de nieuwe kunstvalidatie csv in config middels de ConfiguratieManager
        #   - caw tijdreeksen worden van deze moment geimporteerd (niet met terugwerkende kracht)
        # 4. voor alle tijdreeksen die nog nooit zijn geimporteerd in WIS:
        #     - wij wij maken een extract van historie, die geven we aan Job Verkaik: "hier heb je 1 xml die al die
        #       historosiche data nog een keer bevat
        # 5. Nu kan Inke pas fatsoenlijk validatie regels vastellen (want WIS bevat nu de gehele tijdreeks)
        #   - harde grenzen (bijv HMAX, HMIN):
        #       - voor met name water- en stuwstanden vastellen obv CAW sensorbereik onderstation van een kunstwerk.
        #       - voor streef en stuur: geen idee
        #   - zachte grenzen (bijv SMAX, SMIN):
        #       - vaststellen obv tijdreeks zelf
        # 6. WIS gebruikt deze bandbreedtes om tijdseries te vlaggen.

        description = "controle of attributen van validatieregels overbodig zijn/missen óf verkeerde waarden bevatten"
        logger.info(f"start {self.check_validation_rules.__name__}")
        valid_errors = {
            "internalLocation": [],
            "start": [],
            "eind": [],
            "internalParameters": [],
            "fout_type": [],
            "fout_beschrijving": [],
        }

        for loc_set in (self.hoofdloc, self.subloc, self.waterstandloc, self.mswloc, self.psloc):
            if not loc_set.validation_rules:
                continue

            validation_attributes = loc_set.get_validation_attributes(int_pars=None)
            idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
            idmap_df = pd.DataFrame(data=idmaps)

            data = {int_loc: [df["internalParameter"].values] for int_loc, df in idmap_df.groupby("internalLocation")}
            params_df = pd.DataFrame.from_dict(
                data=data,
                orient="index",  # use 'index' so that data.keys() become df.rows (and not df.columns)
                columns=["internalParameters"],
            )

            location_set_gdf = self.__create_location_set_df(loc_set)

            for idx, row in location_set_gdf.iterrows():
                int_loc = row["LOC_ID"]
                row = row.dropna()
                if int_loc in params_df["internalParameters"]:
                    int_pars = np.unique(params_df.loc[int_loc]["internalParameters"])
                else:
                    int_pars = []

                attribs_required = loc_set.get_validation_attributes(int_pars=int_pars)
                attribs_too_few = [attrib for attrib in attribs_required if attrib not in row.keys()]
                attribs_too_many = [
                    attrib
                    for attrib in validation_attributes
                    if (attrib not in attribs_required) and (attrib in row.keys())
                ]

                for key, value in {"missend": attribs_too_few, "overbodig": attribs_too_many}.items():
                    if len(value) > 0:
                        valid_errors["internalLocation"] += [int_loc]
                        valid_errors["start"] += [row["START"]]
                        valid_errors["eind"] += [row["EIND"]]
                        valid_errors["internalParameters"] += [",".join(int_pars)]
                        valid_errors["fout_type"] += [key]
                        valid_errors["fout_beschrijving"] += [",".join(value)]
                for validation_rule in loc_set.validation_rules:
                    errors = {"fout_type": None, "fout_beschrijving": []}
                    param = validation_rule["parameter"]
                    if any(re.match(pattern=param, string=int_par) for int_par in int_pars):
                        rule = validation_rule["extreme_values"]
                        rule = sort_validation_attribs(rule)
                        if all(key in ["hmax", "hmin"] for key in rule.keys()):
                            for hmin, hmax in zip(rule["hmin"], rule["hmax"]):
                                if all(attrib in row.keys() for attrib in [hmin, hmax]):
                                    if row[hmax] < row[hmin]:
                                        errors["fout_type"] = "waarde"
                                        errors["fout_beschrijving"] += [f"{hmax} < {hmin}"]

                        elif all(key in rule.keys() for key in ["hmax", "smax", "smin", "hmin"]):
                            hmax = rule["hmax"][0]
                            hmin = rule["hmin"][0]
                            for smin, smax in zip(rule["smin"], rule["smax"]):
                                if all(attrib in row.keys() for attrib in [smin, smax]):
                                    if row[smax] <= row[smin]:
                                        errors["fout_type"] = "waarde"
                                        errors["fout_beschrijving"] += [f"{smax} <= {smin}"]

                                    # TODO: hiervoor al ergens checken of alle waarden in row zijn ingevuld,
                                    #  want anders keyerror...
                                    if row[hmax] < row[smax]:
                                        errors["fout_type"] = "waarde"
                                        errors["fout_beschrijving"] += [f"{'hmax'} < {smax}"]

                                    if row[smin] < row[hmin]:
                                        errors["fout_type"] = "waarde"
                                        errors["fout_beschrijving"] += [f"{smin} < {hmin}"]

                    valid_errors["internalLocation"] += [row["LOC_ID"]] * len(errors["fout_beschrijving"])

                    valid_errors["start"] += [row["START"]] * len(errors["fout_beschrijving"])

                    valid_errors["eind"] += [row["EIND"]] * len(errors["fout_beschrijving"])

                    # TODO: ask roger/daniel: geen idee wat hier allemaal gebeurt en waarom..
                    #  stel, int_pars = ['DD.15,F.0,H.R.0,IB.0,Q.G.0']
                    #  dan is ",".join(int_pars) --> 'DD.15,F.0,H.R.0,IB.0,Q.G.0'
                    #  dan is [",".join(int_pars)] * len(errors["fout_beschrijving"]) --> []
                    #  vraag: whuuaaat?! waarom?

                    valid_errors["internalParameters"] += [",".join(int_pars)] * len(errors["fout_beschrijving"])

                    valid_errors["fout_type"] += [errors["fout_type"]] * len(errors["fout_beschrijving"])

                    valid_errors["fout_beschrijving"] += errors["fout_beschrijving"]

        result_df = pd.DataFrame(data=valid_errors).drop_duplicates(keep="first", inplace=False)
        if len(result_df) == 0:
            logger.info("no missing incorrect validation rules")
        else:
            logger.warning(f"{len(result_df)} validation rules contain errors/are missing")
        excel_sheet = ExcelSheet(
            name=sheet_name, description=description, df=result_df, sheet_type=ExcelSheetTypeChoices.output_check
        )
        return excel_sheet

    def check_int_par_ex_par(self, sheet_name: str = "par mismatch") -> ExcelSheet:
        """Check if internal and external parameters are consistent."""
        description = "controle of externe parameters en interne parameters logisch aan elkaar gekoppeld zijn"
        logger.info(f"start {self.check_int_par_ex_par.__name__}")
        par_errors = {
            "internalLocation": [],
            "internalParameter": [],
            "externalParameter": [],
            "fout": [],
        }

        idmaps = self._get_idmaps(idmap_files=["IdOPVLWATER"])
        idmap_df = pd.DataFrame(data=idmaps)
        for idx, row in idmap_df.iterrows():
            error = None
            ext_par = [
                mapping["external"]
                for mapping in constants.PARAMETER_MAPPING
                if re.match(pattern=f'{mapping["internal"]}[0-9]', string=row["internalParameter"])
            ]

            if ext_par:
                if not any(re.match(pattern=par, string=row["externalParameter"]) for par in ext_par):
                    error = "parameter mismatch"
            else:
                error = "pars not included in config"
            if error:
                par_errors["internalLocation"].append(row["internalLocation"])
                par_errors["internalParameter"].append(row["internalParameter"])
                par_errors["externalParameter"].append(row["externalParameter"])
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
        logger.info(f"start {self.check_location_set_errors.__name__}")

        loc_set_errors = {
            "locationId": [],
            "caw_code": [],
            "caw_name": [],
            "csv_file": [],
            "location_name": [],
            "type": [],
            "functie": [],
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
                    "functie": "",
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
                    loc_functie = row["FUNCTIE"]
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
                            pattern=f"[A-Z0-9 ]*_{caw_code}-K_[A-Z0-9 ]*-{sub_type}[0-9]_{loc_functie}",
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
                            par_gdf_xy = par_gdf_row["geometry"].values[0]
                            row_xy = row["geometry"]
                            if not par_gdf_xy.equals(row_xy):
                                error["xy_not_same"] = True

                    if any(error.values()):
                        error["type"] = sub_type
                        error["functie"] = loc_functie

                if loc_set == self.hoofdloc:
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

    def add_input_files_to_results(self) -> None:
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

    def add_paths_to_results(self) -> None:
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

    def add_tab_color_description_to_results(self):
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

    def add_mpt_histtags_new_to_results(self):
        excelsheet = ExcelSheet(
            name="mpt_histtags_new",
            df=self.mpt_histtags_new,
            description="alle meetpunt ids uitgelezen uit de histTags.csv, die niet in de ignore "
            "staan en in de idmapping zijn opgenomen",
            sheet_type=ExcelSheetTypeChoices.output_no_check,
        )
        self.results.add_sheet(excelsheet=excelsheet)

    def run(self):
        self.results.add_sheet(excelsheet=self.check_idmap_sections())
        self.results.add_sheet(excelsheet=self.check_ignored_histtags())
        self.results.add_sheet(excelsheet=self.check_histtags_nomatch())
        self.results.add_sheet(excelsheet=self.check_double_idmaps())
        self.results.add_sheet(excelsheet=self.check_missing_pars())
        self.results.add_sheet(excelsheet=self.check_h_loc())

        # check returns two results
        sheet1, sheet2 = self.check_ex_par_errors_int_loc_missing()
        self.results.add_sheet(excelsheet=sheet1)
        self.results.add_sheet(excelsheet=sheet2)

        self.results.add_sheet(excelsheet=self.check_ex_par_missing())
        self.results.add_sheet(excelsheet=self.check_ex_loc_int_loc())
        self.results.add_sheet(excelsheet=self.check_timeseries_logic())
        self.results.add_sheet(excelsheet=self.check_validation_rules())
        self.results.add_sheet(excelsheet=self.check_int_par_ex_par())
        self.results.add_sheet(excelsheet=self.check_location_set_errors())

        self.add_mpt_histtags_new_to_results()  # TODO: move this below '# add output_no_check sheets'

        # TODO: @renier: remove this integration test
        summary = {sheetname: sheet.nr_rows for sheetname, sheet in self.results.items()}
        validate_expected_summary(new_summary=summary)

        # add output_no_check sheets
        self.add_tab_color_description_to_results()
        self.add_paths_to_results()
        self.add_input_files_to_results()

        # write excel file with check results
        excel_writer = ExcelWriter(results=self.results)
        excel_writer.write()

        # write new csv files
        self.create_opvlwater_hoofdloc_csv_new()
        self.create_opvlwater_subloc_csv_new()
        self.create_waterstandlocaties_csv_new()
