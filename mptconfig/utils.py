from mptconfig import constants
from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

import datetime
import logging
import numpy as np  # noqa numpy comes with geopandas
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


def pd_drop_columns(df: pd.DataFrame, drop_columns: List[str]) -> pd.DataFrame:
    df_drop_columns = [x for x in drop_columns if x in df.columns]
    df.drop(columns=df_drop_columns, axis=1, inplace=True)
    return df


def flatten_nested_list(_list: List[List]) -> List:
    return [item for sublist in _list for item in sublist]


def is_unmeasured_location(
    startdate: Union[str, pd.Timestamp, datetime.date], enddate: Union[str, pd.Timestamp, datetime.date]
) -> bool:
    """A unmeasured (in dutch 'onbemeten') id in subloc that is not in idmapping: no timeseries mapped to it
    = location without a timeseries. This location has been marked with both a dummy start- and enddate in
    the location csvs
    """
    # TODO: remove work-around (3 lines below): 32101230 should be replaced with 22220101 in mpt config csvs
    if str(enddate) in ("32101230", "3210-12-30"):
        assert pd.to_datetime(startdate) == constants.STARTDATE_UNMEASURED_LOC
        return True
    pd_startdate = pd.to_datetime(startdate)
    pd_enddate = pd.to_datetime(enddate)
    start_is_unmeasured = pd_startdate == constants.STARTDATE_UNMEASURED_LOC
    end_is_unmeasured = pd_enddate == constants.ENDDATE_UNMEASURED_LOC
    if start_is_unmeasured != end_is_unmeasured:
        # this is reported in check_dates_loc_sets()
        logger.warning(f"found start={pd_startdate}, end={end_is_unmeasured}")
    return start_is_unmeasured


def idmap2tags(row: pd.Series, idmap: List[Dict]) -> Union[float, List[str]]:
    """Add FEWS-locationIds to histtags in df.apply() method.
    Returns either np.NaN (= float type) or a list with strings (few_locs)."""
    ex_loc, ex_par = row["serie"].split(sep="_", maxsplit=1)
    fews_locs = [
        col["internalLocation"]
        for col in idmap
        if col["externalLocation"] == ex_loc and col["externalParameter"] == ex_par
    ]
    # !! avoid <return fews_locs if fews_locs else [""]> !!
    return fews_locs if fews_locs else np.NaN


def sort_validation_attribs(rule: Dict) -> Dict[str, list]:
    """
    Example:
        rule = {
            'hmax': 'HARDMAX',
            'smax': [
                {'period': 1, 'attribute': 'WIN_SMAX'},
                {'period': 2, 'attribute': 'OV_SMAX'},
                {'period': 3, 'attribute': 'ZOM_SMAX'}
                ],
            'smin': [
                {'period': 1, 'attribute': 'WIN_SMIN'},
                {'period': 2, 'attribute': 'OV_SMIN'},
                {'period': 3, 'attribute': 'ZOM_SMIN'}
                ],
            'hmin': 'HARDMIN'
            }
        _sort_validation_attribs(rule) returns:
        result = {
            'hmax': ['HARDMAX'],
            'smax': ['WIN_SMAX', 'OV_SMAX', 'ZOM_SMAX'],
            'smin': ['WIN_SMIN', 'OV_SMIN', 'ZOM_SMIN'],
            'hmin': ['HARDMIN']
            }
    """
    result = {}
    for key, value in rule.items():
        if isinstance(value, str):
            result[key] = [value]
        elif isinstance(value, list):
            periods = [val["period"] for val in value]
            attribs = [val["attribute"] for val in value]
            result[key] = [attrib for _, attrib in sorted(zip(periods, attribs))]
    return result


def equal_dataframes(expected_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
    """A helper function to ensure that a dataframe check result equals an expected dataframe. """
    # ensure ordered dfs (index and column)
    test_df = test_df.sort_index().sort_index(axis=1)
    expected_df = expected_df.sort_index().sort_index(axis=1)
    return expected_df.equals(test_df)


def pd_read_csv_expect_columns(path: Path, expected_columns: List[str], parse_dates: List[str] = None) -> pd.DataFrame:
    """Flexible pd.read_csv that tries two separators: comma and semi-colon. It verifies the
    panda dataframe column names."""
    assert path.is_file()
    separators = (None, ";") if parse_dates else (",", ";")
    for separator in separators:
        df = pd.read_csv(filepath_or_buffer=path, sep=separator, engine="python", parse_dates=parse_dates)
        if sorted(df.columns) == sorted(expected_columns):
            return df
    raise AssertionError(f"could not read csv {path} with separators ; and ,")
