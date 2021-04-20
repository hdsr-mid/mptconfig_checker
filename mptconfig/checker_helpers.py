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
    when comparing them (WIN, OV, and ZOM) then this applies:
        WIN <= OV <= ZOM
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
    def _compare_two_values(
        cls, row: pd.Series, _lower: str, _upper: str, operator: str, int_pars: List[str], errors: Dict
    ) -> Dict:
        """
        add error is both values are floats and

        eval("1 > 2") --> returns False
        eval("1 <= 2") --> returns True

        """
        default_msg = f"skipping as int_loc {row['LOC_ID']}"
        try:
            value1 = float(row[_lower])
            value2 = float(row[_upper])
        except KeyError:
            logger.debug(f"{default_msg} has no field {_lower} and/or {_upper}")
            return errors
        except (ValueError, TypeError):
            logger.debug(f"{default_msg} fiels {_lower} and/or {_upper} are empty")
            # the absence is already reported in cls.check_attributes_too_few_or_many()
            return errors
        assert operator in ("<", "<=", ">", ">="), f"unexpected: unknown operator {operator}"
        if eval(f"{value1} {operator} {value2}"):
            logger.debug("skipping as two values meet condition")
            return errors
        errors = cls.__add_one_error(
            row=row, int_pars=int_pars, error_type="value", description=f"{_lower} {operator} {_upper}", errors=errors
        )
        return errors

    @classmethod
    def check_hoofd_and_sub_loc(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]) -> Dict:
        """
        hoofd- and sublocations have only 1 value for hmax, hmin, and eventually one for smax, smax
        Examples:
            hoofdlocation "H2.S." has {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}}
            sublocation "H2.R." has {"hmax": "HR2_HMAX", "hmin": "HR2_HMIN"}
            sublocation "Q.B." has {"hmax": "Q_HMAX", "smax": "Q_SMAX", "smin": "Q_SMIN", "hmin": "Q_HMIN"}
        This general rule applies:
            hmin <= smin < smax <= hmax
        in which:
            h = hard
            s = soft

        Compare values separately and only report error if both values are defined (not nan).
        """
        for statement in constants.HLOC_SLOC_VALIDATION_LOGIC:
            _lower, operator, _upper = statement
            _lower_rule = rule.get(_lower, "")  # e.g. from smin to 'HS1_HMIN'
            _upper_rule = rule.get(_upper, "")
            errors = cls._compare_two_values(
                row=row, _lower=_lower_rule, _upper=_upper_rule, operator=operator, int_pars=int_pars, errors=errors
            )
        return errors

    @classmethod
    def check_waterstandstand_loc(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]) -> Dict:
        """
        waterstandlocations have 1 value for hmax, hmin and 3 values for smax and smin
        Examples:
            waterstandloc "H.G." has {
                    "hmax": "HARDMAX",
                    "smax_win": "WIN_SMAX",
                    "smax_ov": "OV_SMAX",
                    "smax_zom": "ZOM_SMAX",
                    "smin_win": "WIN_SMIN",
                    "smin_ov": "OV_SMIN",
                    "smin_zom": "ZOM_SMIN",
                    "hmin": "HARDMIN",
                    }

        We deal with winter (WIN_), transition (OV_ in dutch 'overgang'), and summer (ZOM_).
        For each of them the general rule applies:
            hmin <= smin < smax <= hmax
            in which:
                h = hard
                s = soft
            example: WIN_HMIN <= WIN_SMIN < WIN_SMAX <= WIN_HMAX
        when comparing them (WIN, ZOM, and OV) then this applies:
            ZOM >= OV >= WIN

        Compare values separately and only report error if both values are defined (not nan).
        """
        for statement in constants.WLOC_VALIDATION_LOGIC:
            _lower, operator, _upper = statement
            _lower_rule = rule.get(_lower, "")  # e.g. from smin to 'HS1_HMIN'
            _upper_rule = rule.get(_upper, "")
            errors = cls._compare_two_values(
                row=row, _lower=_lower_rule, _upper=_upper_rule, operator=operator, int_pars=int_pars, errors=errors
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
