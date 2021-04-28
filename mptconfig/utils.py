from datetime import date
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

# TODO: handle end_date dummy check same as start_date
#  below is a tmp work-around because pd.Timestamp(year=3210, month=12, day=30) results in OutOfBoundsDatetime
#  luckily, datetime.date(year=3210, month=12, day=30) is possible. Saves us string comparison mayhem
# TODO: @ask roger: come up with better names
# sublocs without timeseries are unmeasered (dutch 'onbemeten locaties') and have dummy dates
dummy_start_date_unmeasured_loc = pd.Timestamp(year=1900, month=1, day=1)
dummy_end_date_unmeasured_loc = pd.Timestamp(year=2222, month=1, day=1)  # pd.Timestamp.max = '2262-04-11'
dummy_end_date_measured_loc = pd.Timestamp(year=2100, month=1, day=1)


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


def update_h_locs_start_end(
    row: pd.Series, h_locs: np.ndarray, mpt_df: pd.DataFrame
) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """Add startdate and enddate op hoofdloc dataframe with df.apply() method.
    If"""
    # TODO: high prio:
    #  Het lijkt erop dat Daniel een cruciaal punt in de bepaling van de start- en einddatum niet goed verwerkt heeft.
    #  Als er meerdere sublocaties zijn op een hoofdlocatie en enkele (maar niet alle) sublocaties hebben
    #  een dummy-startdatum 19000101 of dummy-einddatum 32101230, dan moeten die dummy-datums niet meegenomen
    #  worden in de bepaling van de start- en einddatum van de hoofdlocatie. Helaas gebeurt dat nu wel.
    #  Kan je kijken of je dit kan oplossen?
    int_loc = row["LOC_ID"]
    if not bool(np.isin(int_loc, h_locs)):
        logger.debug(f"skip update start end as {int_loc} is not a h_loc")
        return row["STARTDATE"], row["ENDDATE"]
    # get all locs at this location:
    brothers_df = mpt_df[mpt_df["LOC_ID"].str.startswith(int_loc[0:-1])]
    if any(brothers_df["STARTDATE"].isin([dummy_start_date_unmeasured_loc])):
        if not all(brothers_df["STARTDATE"].isin([dummy_start_date_unmeasured_loc])):
            logger.debug(f"found some (but not all) dummy_start dates for hloc {int_loc}")
            unmeasured_brothers_df = brothers_df[brothers_df["STARTDATE"] == dummy_start_date_unmeasured_loc]
            # ensure enddate is also a dummy date
            # TODO: activate this assert as soon we come up with a better dummy_end_date_unmeasured_loc
            # assert all(x.to_pydatetime() == dummy_end_date_unmeasured_loc for x in unmeasured_brothers_df["ENDDATE"])
            # remove unmeasured locs
            measured_brothers_df = brothers_df[brothers_df["STARTDATE"] != dummy_start_date_unmeasured_loc]
            earliest_start_date = measured_brothers_df["STARTDATE"].dropna().min()
            latest_end_date = measured_brothers_df["ENDDATE"].dropna().max()
            return earliest_start_date, latest_end_date
    earliest_start_date = brothers_df["STARTDATE"].dropna().min()
    latest_end_date = brothers_df["ENDDATE"].dropna().max()
    return earliest_start_date, latest_end_date


def update_date(row: pd.Series, mpt_df: pd.DataFrame, date_threshold: pd.Timestamp) -> Tuple[str, str]:
    """Return start and end-date, e.g. ('19970101', '21000101'), in df.apply() method."""
    int_loc = row["LOC_ID"]
    # check if int_loc is in pd.Series mpt_df['LOC_ID']
    # watch out! avoid this: "if int_loc in mpt_df['LOC_ID']"
    int_loc_df = mpt_df[mpt_df["LOC_ID"] == int_loc]
    assert len(int_loc_df) in (0, 1)
    if len(int_loc_df) == 1:
        # from series to list
        start_date_list = int_loc_df["STARTDATE"].to_list()
        assert len(start_date_list) == 1
        start_date = start_date_list[0].strftime("%Y%m%d")
        end_date_list = int_loc_df["ENDDATE"].to_list()
        assert len(end_date_list) == 1
        end_date = start_date_list[0]
        if end_date > date_threshold:
            end_date = dummy_end_date_measured_loc
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
