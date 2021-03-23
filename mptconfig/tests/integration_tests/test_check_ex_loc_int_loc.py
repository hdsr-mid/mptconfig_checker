from mptconfig.checker import MptConfigChecker
from mptconfig.excel import ExcelSheet
from mptconfig.excel import ExcelSheetTypeChoices
from mptconfig.tests.patches import patched_path_constants_1
from mptconfig.tests.patches import patched_path_constants_2
from mptconfig.tests.utils import ensure_dataframes_equal

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_df_1 = pd.DataFrame(
    {
        "internalLocation": {
            0: "KW219112",
            1: "KW219120",
            2: "KW219121",
            3: "KW219130",
            4: "KW219131",
            5: "KW431510",
            6: "KW431511",
            7: "KW4315xx",
        },
        "externalLocation": {
            0: "2805",
            1: "2805",
            2: "2805",
            3: "2805",
            4: "2805",
            5: "4803",
            6: "4803",
            7: "4803",
        },
    }
)

expected_df_2 = pd.DataFrame(
    {
        "internalLocation": {0: "KW219112", 1: "KW219120", 2: "KW219121", 3: "KW219130", 4: "KW219131"},
        "externalLocation": {0: "2805", 1: "2805", 2: "2805", 3: "2805", 4: "2805"},
    }
)


def test_check_ex_loc_int_loc_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_ex_loc_int_loc(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 8
    ensure_dataframes_equal(expected_df=expected_df_1, test_df=excelsheet.df)


def test_check_ex_loc_int_loc_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_ex_loc_int_loc(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 5
    ensure_dataframes_equal(expected_df=expected_df_2, test_df=excelsheet.df)
