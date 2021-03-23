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


expected_df_2 = pd.DataFrame(
    {
        "ENDDATE": {0: "2018-12-31 23:30:00\t"},
        "STARTDATE": {0: "2018-03-27 13:15:00"},
        "UNKNOWN_SERIE": {0: "4329_HR2"},
    }
)


def test_check_ignored_histtags_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_ignored_histtags(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 0


def test_check_ignored_histtags_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_ignored_histtags(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 1
    ensure_dataframes_equal(expected_df=expected_df_2, test_df=excelsheet.df)
