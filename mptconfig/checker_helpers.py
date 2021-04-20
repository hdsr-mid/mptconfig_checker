from mptconfig import constants
from typing import Dict
from typing import List
from typing import TypeVar

import logging
import pandas as pd  # noqa pandas comes with geopandas


logger = logging.getLogger(__name__)


PandasDFGroupBy = TypeVar(name="pd.core.groupby.generic.DataFrameGroupBy")  # noqa


class HelperValidationRules:
    @classmethod
    def get_int_pars(cls, idmap_df_grouped_by_intloc: PandasDFGroupBy, int_loc: str):
        try:
            int_loc_group = idmap_df_grouped_by_intloc.get_group(name=int_loc)
            _int_pars = int_loc_group["internalParameter"].unique()
            _int_pars.sort(axis=-1, kind="quicksort", order=None)
        except KeyError:
            logger.debug(f"no problem, int_loc {int_loc} is not in IdOPVLWATER.xml")
            _int_pars = []
        return _int_pars

    @classmethod
    def check_attributes_too_few_or_many(
        cls,
        errors: Dict,
        loc_set: constants.LocationSet,
        row: pd.Series,
        int_pars: List[str],
        validation_attributes,
    ):
        attribs_required = loc_set.get_validation_attributes(int_pars=int_pars)
        attribs_too_few = [attrib for attrib in attribs_required if attrib not in row.keys()]
        attribs_too_many = [
            attrib for attrib in validation_attributes if (attrib not in attribs_required) and (attrib in row.keys())
        ]
        if attribs_too_few:
            errors = cls.add_one_error(
                row=row, int_pars=int_pars, error_type="too_few", description=",".join(attribs_too_few), errors=errors
            )
        if attribs_too_many:
            errors = cls.add_one_error(
                row=row, int_pars=int_pars, error_type="too_many", description=",".join(attribs_too_many), errors=errors
            )
        return errors

    @classmethod
    def check_hmax_hmin(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]):
        for _hmin, _hmax in zip(rule["hmin"], rule["hmax"]):
            if not all(attrib in row.keys() for attrib in [_hmin, _hmax]):
                continue
            if row[_hmax] < row[_hmin]:
                errors = cls.add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_hmax} < {_hmin}", errors=errors
                )
        return errors

    @classmethod
    def check_hmax_hmin_smax_smin(cls, errors: Dict, rule: Dict, row: pd.Series, int_pars: List[str]):
        _hmax = rule["hmax"][0]
        _hmin = rule["hmin"][0]
        for _smin, _smax in zip(rule["smin"], rule["smax"]):
            if not all(attrib in row.keys() for attrib in [_smin, _smax]):
                continue
            if row[_smax] <= row[_smin]:
                errors = cls.add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_smax} <= {_smin}", errors=errors
                )
            if row[_hmax] < row[_smax]:
                errors = cls.add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_hmax} < {_smax}", errors=errors
                )
            if row[_smin] < row[_hmin]:
                errors = cls.add_one_error(
                    row=row, int_pars=int_pars, error_type="value", description=f"{_smin} < {_hmin}", errors=errors
                )
        return errors

    @classmethod
    def add_one_error(
        cls, row: pd.Series, int_pars: List[str], error_type: str, description: str, errors: Dict
    ) -> Dict:
        errors["internalLocation"] += [row["LOC_ID"]]
        errors["start"] += [row["START"]]
        errors["eind"] += [row["EIND"]]
        errors["internalParameters"] += [",".join(int_pars)]
        errors["error_type"] += [error_type]
        errors["error_description"] += [description]
        return errors
