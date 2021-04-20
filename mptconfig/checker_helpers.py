from mptconfig import constants
from typing import Dict
from typing import List
from typing import TypeVar

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


PandasDFGroupBy = TypeVar(name="pd.core.groupby.generic.DataFrameGroupBy")  # noqa


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
    when comparing them (WIN, ZOM, and OV) then:
        ZOM >= OV >= WIN
    """

    @classmethod
    def get_int_pars(cls, idmap_df_grouped_by_intloc: PandasDFGroupBy, int_loc: str) -> List[str]:
        try:
            int_loc_group = idmap_df_grouped_by_intloc.get_group(name=int_loc)
            int_pars = sorted(int_loc_group["internalParameter"].unique().tolist())
        except KeyError:
            logger.debug(f"no problem, int_loc {int_loc} is not in this specific idmapping xml")
            int_pars = []
        return int_pars

    @classmethod
    def check_attributes_too_few_or_many(
        cls,
        errors: Dict,
        loc_set: constants.LocationSet,
        row: pd.Series,
        int_pars: List[str],
        validation_attributes,
    ) -> Dict:
        attribs_required = loc_set.get_validation_attributes(int_pars=int_pars)
        attribs_too_few = [attrib for attrib in attribs_required if attrib not in row.keys()]
        attribs_too_many = [
            attrib for attrib in validation_attributes if (attrib not in attribs_required) and (attrib in row.keys())
        ]
        if attribs_too_few:
            errors = cls.__add_one_error(
                row=row, int_pars=int_pars, error_type="too_few", description=",".join(attribs_too_few), errors=errors
            )
        if attribs_too_many:
            errors = cls.__add_one_error(
                row=row, int_pars=int_pars, error_type="too_many", description=",".join(attribs_too_many), errors=errors
            )
        return errors

    @classmethod
    def check_hmax_hmin(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]) -> Dict:
        """
        for hoofdloc, subloc and waterstandloc this general rul applies:
            hmin <= smin < smax <= hmax
        in which:
            h = hard
            s = soft
        """
        for _hmin, _hmax in zip(rule["hmin"], rule["hmax"]):
            if not all(attrib in row.keys() for attrib in [_hmin, _hmax]):
                continue
            if row[_hmax] < row[_hmin]:
                errors = cls.__add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_hmax} < {_hmin}", errors=errors
                )
        return errors

    @classmethod
    def check_hmax_hmin_smax_smin(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]) -> Dict:
        """
        for hoofdloc, subloc and waterstandloc this general rul applies:
            hmin <= smin < smax <= hmax
        in which:
            h = hard
            s = soft
        """
        hmax = rule["hmax"][0]
        hmin = rule["hmin"][0]
        for _smin, _smax in zip(rule["smin"], rule["smax"]):
            if not all(attrib in row.keys() for attrib in [_smin, _smax]):
                continue
            if row[_smax] <= row[_smin]:
                errors = cls.__add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_smax} <= {_smin}", errors=errors
                )
            if row[hmax] < row[_smax]:
                errors = cls.__add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{hmax} < {_smax}", errors=errors
                )
            if row[_smin] < row[hmin]:
                errors = cls.__add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_smin} < {hmin}", errors=errors
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
