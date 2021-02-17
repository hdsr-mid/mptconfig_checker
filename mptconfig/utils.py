from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar

import logging
import numpy as np  # noqa numpy comes with geopandas
import pandas as pd  # noqa pandas comes with geopandas
import re


PandasDataFrameGroupBy = TypeVar(name="pd.core.groupby.generic.DataFrameGroupBy")

logger = logging.getLogger(__name__)


def idmap2tags(row: pd.Series, idmap: List[Dict]) -> List[str]:
    """Add FEWS-locationIds to histtags in df.apply() method."""
    exloc, expar = row["serie"].split(sep="_", maxsplit=1)
    fews_locs = [
        col["internalLocation"]
        for col in idmap
        if col["externalLocation"] == exloc and col["externalParameter"] == expar
    ]
    return fews_locs if fews_locs else [""]


def get_validation_attribs(validation_rules: List[Dict], int_pars: List[str] = None, loc_type: str = None) -> List[str]:
    """Get attributes from validationRules.

    Example:
        get_validation_attribs(
            validation_rules= [
                {
                    'parameter': 'H.R.',
                    'extreme_values': {'hmax': 'HR1_HMAX', 'hmin': 'HR1_HMIN'}
                },
                {
                    'parameter': 'H2.R.',
                    'extreme_values': {'hmax': 'HR2_HMAX', 'hmin': 'HR2_HMIN'}
                },
                etc..
            ]

        returns:
            [
            'HR1_HMAX', 'HR1_HMIN', 'HR2_HMAX', 'HR2_HMIN', 'HR3_HMAX', 'HR3_HMIN', 'FRQ_HMAX',
            'FRQ_HMIN', 'HEF_HMAX', 'HEF_HMIN', 'PERC_HMAX', 'PERC_SMAX', 'PERC_SMIN', 'PERC_HMIN',
            'PERC2_HMAX', 'PERC2_SMAX', 'PERC2_SMIN', 'PERC2_HMIN', 'TT_HMAX', 'TT_HMIN'
            ]

    """
    if int_pars is None:
        int_pars = [rule["parameter"] for rule in validation_rules]
    result = []
    for rule in validation_rules:
        if "type" in rule.keys():
            # TODO: @daniel, wat is loc_type? wordt in geen enkele call meegegeven.
            #  Dus loc_type is None, dus hieronder staat: if rule["type'] == None ?
            #  omdat rule een Dict[str:str] is, neem ik aan dat loc_type een string is. Klopt die aanname?
            if rule["type"] == loc_type:
                if any(re.match(rule["parameter"], int_par) for int_par in int_pars):
                    for key, attribute in rule["extreme_values"].items():
                        if isinstance(attribute, list):
                            result += [value["attribute"] for value in attribute]
                        else:
                            result += [attribute]
        elif any(re.match(rule["parameter"], int_par) for int_par in int_pars):
            for key, attribute in rule["extreme_values"].items():
                if isinstance(attribute, list):
                    result += [value["attribute"] for value in attribute]
                else:
                    result += [attribute]
    return result


def update_hlocs(row: pd.Series, h_locs: np.ndarray, mpt_df: pd.DataFrame) -> Tuple[pd.Timestamp, pd.Timestamp]:
    """Add startdate and enddate op hoofdloc dataframe with df.apply() method."""
    loc_id = row.name
    start_date = row["STARTDATE"]
    end_date = row["ENDDATE"]

    if loc_id in h_locs:
        start_date = mpt_df[mpt_df.index.str.contains(loc_id[0:-1])]["STARTDATE"].dropna().min()
        end_date = mpt_df[mpt_df.index.str.contains(loc_id[0:-1])]["ENDDATE"].dropna().max()
    return start_date, end_date


def update_date(row: pd.Series, mpt_df: pd.DataFrame, date_threshold: pd.Timestamp) -> Tuple[str, str]:
    """Return start and end-date, e.g. ('19970101', '21000101'), in df.apply() method."""
    int_loc = row["LOC_ID"]
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
    # TODO: @daniel, waarom generator? kunnen er meerdere updated_histtags per panda cel worden weggeschreven?
    # TODO: @daniel, is return value altijd str?
    # TODO: @daniel, kan len(updated_histtag) > 1 ??
    # TODO: @daniel, bij idmap2tags retourneer je ergens np.Nan of een [

    # TODO: @renier: remove comment
    # renier zn code
    updated_histtag = [
        df.sort_values("total_max_end_dt", ascending=False)["serie"].values[0]
        for loc_id, df in grouper
        if loc_id == row["LOC_ID"]
    ]
    assert len(updated_histtag) in [0, 1], (
        f"this should not happen, length of updated_histtag should be 0 or 1. " f"updated_histtag={updated_histtag}"
    )
    updated_histtag_str = updated_histtag[0] if updated_histtag else ""
    return updated_histtag_str

    # TODO: @renier: remove code below?
    # daniel zn code
    # return next(
    #     (
    #         df.sort_values("total_max_end_dt", ascending=False)["serie"].values[0]
    #         for loc_id, df in grouper
    #         if loc_id == row["LOC_ID"]
    #     ),
    #     None,
    # )


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
