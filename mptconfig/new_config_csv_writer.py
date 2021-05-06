from mptconfig import constants
from mptconfig.checker_helpers import NewValidationCsv
from mptconfig.constants import MAX_DIFF
from mptconfig.fews_utilities import FewsConfig
from mptconfig.utils import is_unmeasured_location
from mptconfig.utils import pd_drop_columns
from pathlib import Path
from typing import List
from typing import Tuple
from typing import TypeVar

import geopandas as gpd
import logging
import numpy as np
import pandas as pd


PandasDataFrameGroupBy = TypeVar(name="pd.core.groupby.generic.DataFrameGroupBy")  # noqa

logger = logging.getLogger(__name__)


class NewConfigCsvWriter:
    def __init__(
        self,
        hoofdloc: constants.HoofdLocationSet,
        subloc: constants.SubLocationSet,
        waterstandloc: constants.WaterstandLocationSet,
        mpt_histtags: pd.DataFrame,
        validation_csvs_new: List[NewValidationCsv],
        do_write_new_hoofdloc: bool,
    ):
        self.hoofdloc = hoofdloc
        self.subloc = subloc
        self.waterstandloc = waterstandloc
        self.mpt_histtags = mpt_histtags
        self._mpt_histtags_new = None
        self.validation_csvs_new = validation_csvs_new
        self.do_write_new_hoofdloc = do_write_new_hoofdloc

    @staticmethod
    def update_h_locs_start_end(
        row: pd.Series, h_locs: np.ndarray, mpt_df: pd.DataFrame
    ) -> Tuple[pd.Timestamp, pd.Timestamp]:
        """Get the earliest startdate and last enddate from all grouped sublocs (per hoofdloc).
        We exclude startdate and enddate from unmeasured sublocs if not all sublocs are unmeasured."""
        int_loc = row["LOC_ID"]
        if not bool(np.isin(int_loc, h_locs)):
            logger.debug(f"skip update start end as {int_loc} is not a h_loc")
            return row["STARTDATE"], row["ENDDATE"]
        # get all locs at this location:
        brothers_df = mpt_df[mpt_df["LOC_ID"].str.startswith(int_loc[0:-1])]
        brothers_df["is_unmeasured"] = brothers_df.apply(
            func=lambda x: is_unmeasured_location(startdate=x["STARTDATE"], enddate=x["ENDDATE"]), axis=1
        )
        if any(brothers_df["is_unmeasured"]) and not all(brothers_df["is_unmeasured"]):
            logger.debug(f"some - but not all - sub_locs are unmeasured for hoofdloc {int_loc}")
            # continue only with measured locations (rows where is_unmeasured is False)
            brothers_df = brothers_df[brothers_df["is_unmeasured"] == False]  # noqa
        earliest_start_date = brothers_df["STARTDATE"].dropna().min()
        latest_end_date = brothers_df["ENDDATE"].dropna().max()
        return earliest_start_date, latest_end_date

    @property
    def mpt_histtags_new(self) -> pd.DataFrame:
        """Convert histTag-ids to mpt-ids. Alle meetpunt ids uitgelezen uit de histTags.csv, die niet
        in de ignore staan en in de idmapping zijn opgenomen. This property is used to create new config
        csvs (hoofdloc, subloc, and waterstandloc) to determine start- and enddate."""
        if self._mpt_histtags_new is not None:
            return self._mpt_histtags_new
        loc_id_col = "LOC_ID"
        start_col = "STARTDATE"
        end_col = "ENDDATE"
        pd_start_col = "pd_start"
        pd_end_col = "pd_end"
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
            func=self.update_h_locs_start_end, args=[h_locs, mpt_df], axis=1, result_type="expand"
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

    @staticmethod
    def update_histtag(row: pd.Series, grouper: PandasDataFrameGroupBy) -> str:
        """Assign last histTag to waterstandsloc in df.apply method.
        row['LOC_ID'] is e.g. 'OW100101'
        updated_histtag_str is e.g. '1001_HO1'
        """
        # TODO: this takes forever, use masks!
        updated_histtag = [
            df.sort_values("total_max_end_dt", ascending=False)["serie"].values[0]
            for loc_id, df in grouper
            if loc_id == row["LOC_ID"]
        ]
        if len(updated_histtag) == 0:
            return ""
        elif len(updated_histtag) == 1:
            return updated_histtag[0]
        raise AssertionError(
            f"this should not happen, length of updated_histtag should be 0 or 1. updated_histtag={updated_histtag}"
        )

    def _update_staff_gauge(self, row: pd.Series) -> Tuple[str, str]:
        """Assign upstream and downstream staff gauges to subloc."""
        result = {"HBOV": "", "HBEN": ""}
        for key in result.keys():
            df = self.waterstandloc.geo_df.loc[self.waterstandloc.geo_df["LOC_ID"] == row[key]]
            if not df.empty:
                result[key] = df["PEILSCHAAL"].values[0]
        return result["HBOV"], result["HBEN"]

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
        return df

    @staticmethod
    def _ensure_only_original_columns(df: pd.DataFrame, loc_set: constants.LocationSet) -> pd.DataFrame:
        current_columns = df.columns.to_list()
        original_columns = loc_set.geo_df_original.columns.to_list()
        # remove 'geometry' as it was added during loading in FewsConfig
        original_columns.remove("geometry")
        too_few = set(original_columns).difference(set(current_columns))
        too_many = set(current_columns).difference(set(original_columns))
        assert not too_few, f"new csv {loc_set.name} has too_few columns {too_few}"
        logger.debug(f"drop columns {too_many} for new csv {loc_set.name}")
        df = pd_drop_columns(df=df, drop_columns=list(too_many))
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
        # GeoDataFrame is a Datafame with a geometry column
        df = gdf.drop("geometry", axis=1)
        return df

    def _write_new_opvlwater_hoofdloc_csv(self) -> None:
        """Write HoofdLocationSet.geo_df to csv."""
        logger.info(f"creating new csv {self.hoofdloc.name}")
        df = self._validate_geom(gdf=self.hoofdloc.geo_df)
        df = self._update_enddate_new_csv(df=df, file_name=self.hoofdloc.name)
        df = self._ensure_only_original_columns(df=df, loc_set=self.hoofdloc)
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
        df = self._ensure_only_original_columns(df=df, loc_set=self.subloc)
        self._df_to_csv(df=df, file_name=self.subloc.name)

    def _write_new_waterstandlocaties_csv(self) -> None:
        """ Write WaterstandLocationSet.geo_df to csv."""
        logger.info(f"creating new csv {self.waterstandloc.name}")
        df = self._validate_geom(gdf=self.waterstandloc.geo_df)
        df = self._update_enddate_new_csv(df=df, file_name=self.waterstandloc.name)
        # TODO: why not use mpt_histtags_new?
        grouper = self.mpt_histtags.groupby(["LOC_ID"])
        # leave it HIST_TAG (instead of HISTTAG), as that is what OPVLWATER_WATERSTANDEN_AUTO.csv expects
        df["HIST_TAG"] = df.apply(func=self.update_histtag, args=[grouper], axis=1, result_type="expand")
        df = self._ensure_only_original_columns(df=df, loc_set=self.waterstandloc)
        self._df_to_csv(df=df, file_name=self.waterstandloc.name)

    def run(self):
        self._write_new_opvlwater_subloc_csv()
        self._write_new_waterstandlocaties_csv()
        # optional new hoofdloc
        if self.do_write_new_hoofdloc:
            self._write_new_opvlwater_hoofdloc_csv()
        else:
            logger.warning(f"skip creating {self.hoofdloc.name}.csv as hoofdloc was not updated")
        # optional new validation csvs
        for new_validation_csv in self.validation_csvs_new:
            filename = new_validation_csv.orig_filepath.name
            logger.info(f"creating new csv {filename}")
            self._df_to_csv(df=new_validation_csv.df, file_name=filename)
