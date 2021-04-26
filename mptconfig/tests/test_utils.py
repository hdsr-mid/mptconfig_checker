from mptconfig.utils import dummy_start_date_unmeasured_loc
from mptconfig.utils import update_h_locs_start_end

import numpy as np
import pandas as pd  # noqa pandas comes with geopandas


def test_update_h_locs_start_end_all_measured_sub_loc():
    """ mpt_df has 3 sublocs of which one is unmeasured (so 1 row with dummy dates). """
    row = pd.Series(
        data={
            "LOC_ID": "KW100110",
            "STARTDATE": pd.Timestamp("1999-12-01 00:00:00"),
            "ENDDATE": pd.Timestamp("2020-09-30 23:45:00"),
        }
    )
    h_locs = np.array("KW100110")
    mpt_df = pd.DataFrame(
        data={
            "LOC_ID": {0: "KW100111", 5: "KW100112", 6: "KW100110"},
            "STARTDATE": {
                0: pd.Timestamp("1997-01-01 00:00:00"),
                5: pd.Timestamp("2013-05-05 00:00:00"),
                6: pd.Timestamp("1999-12-01 00:00:00"),
            },
            "ENDDATE": {
                0: pd.Timestamp("2020-09-30 23:45:00"),
                5: pd.Timestamp("2020-09-30 23:45:00"),
                6: pd.Timestamp("2020-09-30 23:45:00"),
            },
        }
    )
    start_date, end_date = update_h_locs_start_end(row=row, h_locs=h_locs, mpt_df=mpt_df)
    assert start_date == pd.Timestamp(year=1997, month=1, day=1)
    assert end_date == pd.Timestamp(year=2020, month=9, day=30, hour=23, minute=45)


def test_update_h_locs_start_end_1_unmeasured_sub_locs():
    """ mpt_df has no unmeasured sublocations (so 1 row with dummy dates). """
    row = pd.Series(
        data={
            "LOC_ID": "KW100110",
            "STARTDATE": pd.Timestamp("1999-12-01 00:00:00"),
            "ENDDATE": pd.Timestamp("2020-09-30 23:45:00"),
        }
    )
    h_locs = np.array("KW100110")
    mpt_df = pd.DataFrame(
        data={
            "LOC_ID": {0: "KW100111", 5: "KW100112", 6: "KW100110"},
            "STARTDATE": {
                0: dummy_start_date_unmeasured_loc,
                5: pd.Timestamp("2013-05-05 00:00:00"),
                6: pd.Timestamp("1999-12-01 00:00:00"),
            },
            "ENDDATE": {
                0: pd.Timestamp(
                    "2020-09-30 23:45:00"
                ),  # noqa TODO: this must be pd.Timestamp(dummy_end_date_unmeasured_loc)
                5: pd.Timestamp("2020-09-30 23:45:00"),
                6: pd.Timestamp("2020-09-30 23:45:00"),
            },
        }
    )
    start_date, end_date = update_h_locs_start_end(row=row, h_locs=h_locs, mpt_df=mpt_df)
    assert start_date == pd.Timestamp(year=1999, month=12, day=1)
    assert end_date == pd.Timestamp(year=2020, month=9, day=30, hour=23, minute=45)


def test_update_h_locs_start_end_only_unmeasured_sub_locs():
    """ mpt_df has only unmeasured sublocations (so only dummy dates). """
    row = pd.Series(
        data={
            "LOC_ID": "KW100110",
            "STARTDATE": pd.Timestamp("1999-12-01 00:00:00"),
            "ENDDATE": pd.Timestamp("2020-09-30 23:45:00"),
        }
    )
    h_locs = np.array("KW100110")
    mpt_df = pd.DataFrame(
        data={
            "LOC_ID": {0: "KW100111", 5: "KW100112", 6: "KW100110"},
            "STARTDATE": {
                0: dummy_start_date_unmeasured_loc,
                5: dummy_start_date_unmeasured_loc,
                6: dummy_start_date_unmeasured_loc,
            },
            "ENDDATE": {
                0: pd.Timestamp(
                    "2020-09-30 23:45:00"
                ),  # noqa TODO: this must be pd.Timestamp(dummy_end_date_unmeasured_loc)
                5: pd.Timestamp(
                    "2020-09-30 23:45:00"
                ),  # noqa TODO: this must be pd.Timestamp(dummy_end_date_unmeasured_loc)
                6: pd.Timestamp(
                    "2020-09-30 23:45:00"
                ),  # noqa TODO: this must be pd.Timestamp(dummy_end_date_unmeasured_loc)
            },
        }
    )
    start_date, end_date = update_h_locs_start_end(row=row, h_locs=h_locs, mpt_df=mpt_df)
    assert start_date == dummy_start_date_unmeasured_loc
    # TODO: end_date must equal pd.Timestamp(dummy_end_date_unmeasured_loc)
