from mptconfig.checker import MptConfigChecker
from mptconfig.excel import ExcelSheet
from mptconfig.excel import ExcelSheetTypeChoices
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from mptconfig.tests.utils import ensure_dataframes_equal

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_df_1_and_2 = pd.DataFrame(
    {
        "ENDDATE": {
            0: pd.Timestamp("2018-04-10 14:00:15"),
            1: pd.Timestamp("2020-05-19 09:30:00"),
            2: pd.Timestamp("2020-09-30 23:45:00"),
            3: pd.Timestamp("2020-09-30 02:30:48"),
            4: pd.Timestamp("2003-12-31 23:45:00"),
            5: pd.Timestamp("2018-03-27 05:45:10"),
            6: pd.Timestamp("2018-03-27 13:00:30"),
            7: pd.Timestamp("2020-09-30 23:02:40"),
            8: pd.Timestamp("2020-09-30 23:45:00"),
            9: pd.Timestamp("2020-09-30 23:45:00"),
            10: pd.Timestamp("2018-04-11 05:45:09"),
            11: pd.Timestamp("2020-09-30 22:58:18"),
            12: pd.Timestamp("2020-05-05 09:45:00"),
            13: pd.Timestamp("2019-06-17 05:46:36"),
            14: pd.Timestamp("2020-09-30 23:46:30"),
        },
        "STARTDATE": {
            0: pd.Timestamp("2018-03-27 02:30:20"),
            1: pd.Timestamp("2018-06-20 16:26:18"),
            2: pd.Timestamp("2018-04-15 00:00:00"),
            3: pd.Timestamp("2018-04-15 02:30:47"),
            4: pd.Timestamp("1991-01-01 00:00:00"),
            5: pd.Timestamp("2014-05-26 13:20:20"),
            6: pd.Timestamp("2015-07-13 15:30:11"),
            7: pd.Timestamp("2019-02-25 15:04:30"),
            8: pd.Timestamp("2018-03-27 13:15:00"),
            9: pd.Timestamp("2018-06-24 00:00:00"),
            10: pd.Timestamp("2018-03-27 05:45:10"),
            11: pd.Timestamp("2018-03-27 13:00:30"),
            12: pd.Timestamp("2019-05-21 08:30:00"),
            13: pd.Timestamp("2019-04-23 10:12:06"),
            14: pd.Timestamp("2020-01-14 16:29:15"),
        },
        "UNKNOWN_SERIE": {
            0: "1010_ES1",
            1: "1013_HS3",
            2: "1807_HR1",
            3: "1807_HS1",
            4: "313_V1",
            5: "315_ES1",
            6: "322_ES2",
            7: "3230_Q4",
            8: "4310_Q4",
            9: "4310_SP1",
            10: "4315_ES1",
            11: "4322_ES2",
            12: "4331_HS4",
            13: "4408_ES2",
            14: "4813_Q2",
        },
    }
)


def test_check_missing_histtags_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_missing_histtags(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 15
    ensure_dataframes_equal(expected_df=expected_df_1_and_2, test_df=excelsheet.df)


def test_check_missing_histtags_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_missing_histtags(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 15
    ensure_dataframes_equal(expected_df=expected_df_1_and_2, test_df=excelsheet.df)
