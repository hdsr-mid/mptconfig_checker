from mptconfig.checker import MptConfigChecker
from mptconfig.excel import ExcelSheet
from mptconfig.excel import ExcelSheetTypeChoices
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from mptconfig.utils import equal_dataframes

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


expected_df_1_and_2 = pd.DataFrame(
    {"int_locs": {0: "KW4315xx", 1: "KW4322xx"}, "error_type": {0: "not in any csv", 1: "not in any csv"}}
)


def test_check_idmap_int_loc_in_csv_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_idmap_int_loc_in_csv(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 2
    assert equal_dataframes(expected_df=expected_df_1_and_2, test_df=excelsheet.df)


def test_check_idmap_int_loc_in_csv_2(patched_path_constants_1):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_idmap_int_loc_in_csv(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 2
    assert equal_dataframes(expected_df=expected_df_1_and_2, test_df=excelsheet.df)
