from mptconfig.checker import MptConfigChecker
from mptconfig.excel import ExcelSheet
from mptconfig.excel import ExcelSheetTypeChoices
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from mptconfig.utils import equal_dataframes
from unittest.mock import patch

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


expected_df_1_and_2 = pd.DataFrame(
    {
        "internalLocation": {0: "KW101313", 1: "KW440910"},
        "internalParameter": {0: "H.G.0", 1: "H.G.0"},
        "externalParameter": {0: "HR3", 1: "HS1"},
        "fout": {0: "parameter mismatch", 1: "parameter mismatch"},
    }
)


def new_get_idmaps_with_some_errors(*args, **kwargs):
    return [
        {  # orig was H.G.0
            "externalLocation": "2161",
            "externalParameter": "HO2",
            "internalLocation": "KW216112",
            "internalParameter": "H.R.0",
        },
        {  # orig was H.G.0
            "externalLocation": "2164",
            "externalParameter": "HO2",
            "internalLocation": "KW216411",
            "internalParameter": "H.S.0",
        },
        {  # orig was H.G.0
            "externalLocation": "2166",
            "externalParameter": "HO2",
            "internalLocation": "KW216611",
            "internalParameter": "HG.0",
        },
        {  # orig was H.R.0
            "externalLocation": "2161",
            "externalParameter": "HR1",
            "internalLocation": "KW216113",
            "internalParameter": "H.S.0",
        },
        {  # orig was H.S.0
            "externalLocation": "2161",
            "externalParameter": "HS1",
            "internalLocation": "KW216110",
            "internalParameter": "H.G.0",
        },
        {  # orig was H.S.0
            "externalLocation": "2162",
            "externalParameter": "HS1",
            "internalLocation": "KW216210",
            "internalParameter": "H.S",
        },
        {  # orig was DD.15
            "externalLocation": "2161",
            "externalParameter": "I1B",
            "internalLocation": "KW216113",
            "internalParameter": "D.D15",
        },
        {  # orig was DD.15
            "externalLocation": "2161",
            "externalParameter": "I2B",
            "internalLocation": "KW216114",
            "internalParameter": "IB.0",
        },
        {  # orig was IB.0
            "externalLocation": "2161",
            "externalParameter": "IB1",
            "internalLocation": "KW216113",
            "internalParameter": "I.B.0",
        },
        {  # orig was IB.0
            "externalLocation": "2161",
            "externalParameter": "IB2",
            "internalLocation": "KW216114",
            "internalParameter": "IB2.0",
        },
        {  # orig was Q.G.0
            "externalLocation": "2161",
            "externalParameter": "Q1",
            "internalLocation": "KW216113",
            "internalParameter": "Q.G",
        },
        {  # orig was Q.G.0
            "externalLocation": "2161",
            "externalParameter": "Q1",
            "internalLocation": "KW216114",
            "internalParameter": "Q.B.0",
        },
        {  # orig was Q.G.0
            "externalLocation": "2161",
            "externalParameter": "Q3",
            "internalLocation": "KW216115",
            "internalParameter": "Q.G.15",
        },
        {  # orig was F.0
            "externalLocation": "2162",
            "externalParameter": "FQ1",
            "internalLocation": "KW216212",
            "internalParameter": "F.Q.0",
        },
        {  # orig was F.0
            "externalLocation": "2162",
            "externalParameter": "FQ2",
            "internalLocation": "KW216222",
            "internalParameter": "F0",
        },
        {  # orig was Hk.0
            "externalLocation": "2162",
            "externalParameter": "SW1",
            "internalLocation": "KW216213",
            "internalParameter": "H.k.0",
        },
        {  # orig was Hk.0
            "externalLocation": "2162",
            "externalParameter": "SW1",
            "internalLocation": "KW216214",
            "internalParameter": "HK.0",
        },
        {  # orig was ES.0
            "externalLocation": "2163",
            "externalParameter": "ES1",
            "internalLocation": "KW216311",
            "internalParameter": "E.S.0",
        },
        {  # orig was ES.0
            "externalLocation": "2166",
            "externalParameter": "ES1",
            "internalLocation": "KW216613",
            "internalParameter": "E.S",
        },
        {  # orig was Hh.0
            "externalLocation": "2166",
            "externalParameter": "SS1",
            "internalLocation": "KW216613",
            "internalParameter": "H.h.0",
        },
        {  # orig was Hh.0
            "externalLocation": "2166",
            "externalParameter": "SS1",
            "internalLocation": "KW216614",
            "internalParameter": "H.H.0",
        },
    ]


expected_df_with_manual_errors = pd.DataFrame(
    {
        "internalLocation": {
            0: "KW216112",
            1: "KW216411",
            2: "KW216611",
            3: "KW216113",
            4: "KW216110",
            5: "KW216210",
            6: "KW216113",
            7: "KW216114",
            8: "KW216113",
            9: "KW216114",
            10: "KW216113",
            11: "KW216114",
            12: "KW216212",
            13: "KW216222",
            14: "KW216213",
            15: "KW216214",
            16: "KW216311",
            17: "KW216613",
            18: "KW216613",
            19: "KW216614",
        },
        "internalParameter": {
            0: "H.R.0",
            1: "H.S.0",
            2: "HG.0",
            3: "H.S.0",
            4: "H.G.0",
            5: "H.S",
            6: "D.D15",
            7: "IB.0",
            8: "I.B.0",
            9: "IB2.0",
            10: "Q.G",
            11: "Q.B.0",
            12: "F.Q.0",
            13: "F0",
            14: "H.k.0",
            15: "HK.0",
            16: "E.S.0",
            17: "E.S",
            18: "H.h.0",
            19: "H.H.0",
        },
        "externalParameter": {
            0: "HO2",
            1: "HO2",
            2: "HO2",
            3: "HR1",
            4: "HS1",
            5: "HS1",
            6: "I1B",
            7: "I2B",
            8: "IB1",
            9: "IB2",
            10: "Q1",
            11: "Q1",
            12: "FQ1",
            13: "FQ2",
            14: "SW1",
            15: "SW1",
            16: "ES1",
            17: "ES1",
            18: "SS1",
            19: "SS1",
        },
        "fout": {
            0: "parameter mismatch",
            1: "parameter mismatch",
            2: "in_par has no allowed ex_pars",
            3: "parameter mismatch",
            4: "parameter mismatch",
            5: "in_par has no allowed ex_pars",
            6: "in_par has no allowed ex_pars",
            7: "parameter mismatch",
            8: "in_par has no allowed ex_pars",
            9: "in_par has no allowed ex_pars",
            10: "in_par has no allowed ex_pars",
            11: "in_par has no allowed ex_pars",
            12: "in_par has no allowed ex_pars",
            13: "in_par has no allowed ex_pars",
            14: "in_par has no allowed ex_pars",
            15: "in_par has no allowed ex_pars",
            16: "in_par has no allowed ex_pars",
            17: "in_par has no allowed ex_pars",
            18: "in_par has no allowed ex_pars",
            19: "in_par has no allowed ex_pars",
        },
    }
)


def test_check_int_par_ex_par_mismatch_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_int_par_ex_par_mismatch(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 0


def test_check_int_par_ex_par_mismatch_patched_method(patched_path_constants_1):
    """integration test with patched paths 1 and patched _get_idmaps()"""
    # Instead of changing the data in the config (patched_path_constants_1.fews_config.value.path), we alter
    # private method MptConfigChecker._get_idmaps(). Why? No int_ex_par_mismatches exists in the reference data,
    # so we need to create some errors + we do not want these errors affect other tests.
    assert hasattr(MptConfigChecker, "_get_idmaps")
    with patch.object(MptConfigChecker, "_get_idmaps", new=new_get_idmaps_with_some_errors):
        meetpunt_config = MptConfigChecker()
        assert meetpunt_config._get_idmaps() == new_get_idmaps_with_some_errors()
        excelsheet = meetpunt_config.check_int_par_ex_par_mismatch(sheet_name="blabla")
        assert isinstance(excelsheet, ExcelSheet)
        assert excelsheet.name == "blabla"
        assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
        assert excelsheet.nr_rows == 20
        assert equal_dataframes(expected_df=expected_df_with_manual_errors, test_df=excelsheet.df)


def test_check_int_par_ex_par_mismatch_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_int_par_ex_par_mismatch(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 2
    assert equal_dataframes(expected_df=expected_df_1_and_2, test_df=excelsheet.df)
