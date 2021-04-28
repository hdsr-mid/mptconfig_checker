from datetime import date
from mptconfig.constants import DUMMY_ENDDATE_UNMEASURED_LOC
from mptconfig.constants import DUMMY_STARTDATE_UNMEASURED_LOC
from mptconfig.utils import is_unmeasured_location
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
                0: DUMMY_STARTDATE_UNMEASURED_LOC,
                5: pd.Timestamp("2013-05-05 00:00:00"),
                6: pd.Timestamp("1999-12-01 00:00:00"),
            },
            "ENDDATE": {
                0: DUMMY_ENDDATE_UNMEASURED_LOC,
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
                0: DUMMY_STARTDATE_UNMEASURED_LOC,
                5: DUMMY_STARTDATE_UNMEASURED_LOC,
                6: DUMMY_STARTDATE_UNMEASURED_LOC,
            },
            "ENDDATE": {
                0: DUMMY_ENDDATE_UNMEASURED_LOC,
                5: DUMMY_ENDDATE_UNMEASURED_LOC,
                6: DUMMY_ENDDATE_UNMEASURED_LOC,
            },
        }
    )
    start_date, end_date = update_h_locs_start_end(row=row, h_locs=h_locs, mpt_df=mpt_df)
    assert start_date == DUMMY_STARTDATE_UNMEASURED_LOC
    assert end_date == DUMMY_ENDDATE_UNMEASURED_LOC


def test_is_unmeasured_location():
    start = pd.Timestamp(year=2000, month=1, day=1)
    end = pd.Timestamp(year=2001, month=1, day=1)
    assert not is_unmeasured_location(startdate=start, enddate=end)

    # other dtypes (str, datetime.date) is also possible
    start = "19901230"
    end = date(year=2002, month=1, day=2)
    assert not is_unmeasured_location(startdate=start, enddate=end)

    # check unmeasured loc (new dummy enddate)
    start = pd.Timestamp(year=1900, month=1, day=1)
    end = "22220101"
    assert is_unmeasured_location(startdate=start, enddate=end)

    # TODO: this should raise pd.errors.OutOfBoundsDatetime
    # check unmeasured loc (old dummy enddate)
    start = pd.Timestamp(year=1900, month=1, day=1)
    end = "32101230"
    assert is_unmeasured_location(startdate=start, enddate=end)

    #
    df = pd.DataFrame(
        data={
            "LOC_ID": {7: "KW100120", 8: "KW100121"},
            "STARTDATE": {7: pd.Timestamp(year=1900, month=1, day=1), 8: pd.Timestamp("2012-03-21 14:00:00")},
            "ENDDATE": {7: pd.Timestamp(year=2222, month=1, day=1), 8: pd.Timestamp("2020-09-30 23:49:37")},
        }
    )
    df["is_unmeasured"] = df.apply(
        func=lambda x: is_unmeasured_location(startdate=x["STARTDATE"], enddate=x["ENDDATE"]), axis=1
    )
    assert df["is_unmeasured"].to_list() == [True, False]
