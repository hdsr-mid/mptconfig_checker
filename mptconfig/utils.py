from pathlib import Path
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar
from typing import Union

import logging
import numpy as np  # noqa numpy comes with geopandas
import pandas as pd  # noqa pandas comes with geopandas


PandasDataFrameGroupBy = TypeVar(name="pd.core.groupby.generic.DataFrameGroupBy")

logger = logging.getLogger(__name__)


def flatten_nested_list(_list: List[List]) -> List:
    return [item for sublist in _list for item in sublist]


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


def update_h_locs(row: pd.Series, h_locs: np.ndarray, mpt_df: pd.DataFrame) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """Add startdate and enddate op hoofdloc dataframe with df.apply() method."""
    if not bool(np.isin(row["LOC_ID"], h_locs)):
        return row["STARTDATE"], row["ENDDATE"]
    # get all locs at this location:
    brothers_df = mpt_df[mpt_df["LOC_ID"].str.startswith(row["LOC_ID"][0:-1])]
    earliest_start_date = brothers_df["STARTDATE"].dropna().min()
    latest_end_date = brothers_df["ENDDATE"].dropna().max()
    return earliest_start_date, latest_end_date


def update_date(row: pd.Series, mpt_df: pd.DataFrame, date_threshold: pd.Timestamp) -> Tuple[str, str]:
    """Return start and end-date, e.g. ('19970101', '21000101'), in df.apply() method."""
    int_loc = row["LOC_ID"]
    # TODO: fix index
    if int_loc in mpt_df.index:
        start_date = mpt_df.loc[int_loc]["STARTDATE"].strftime("%Y%m%d")
        end_date = mpt_df.loc[int_loc]["ENDDATE"]
        if end_date > date_threshold:
            end_date = pd.Timestamp(year=2100, month=1, day=1)
        end_date = end_date.strftime("%Y%m%d")
    else:
        start_date = row["START"]
        end_date = row["EIND"]
    return start_date, end_date


def update_histtag(row: pd.Series, grouper: PandasDataFrameGroupBy) -> str:
    """Assign last histTag to waterstandsloc in df.apply method.
    row['LOC_ID'] is e.g. 'OW100101'
    updated_histtag_str is e.g. '1001_HO1'
    """
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


def panda_read_csv(path: Path, expected_columns: List[str], parse_dates: List[str] = None) -> pd.DataFrame:
    """Flexible pd.read_csv that tries two separators: comma and semi-colon. It verifies the
    panda dataframe column names."""
    assert path.is_file()
    separators = (None, ";") if parse_dates else (",", ";")
    for separator in separators:
        df = pd.read_csv(filepath_or_buffer=path, sep=separator, engine="python", parse_dates=parse_dates)
        if sorted(df.columns) == sorted(expected_columns):
            return df
    raise AssertionError(f"could not read csv {path} with separators ; and ,")
