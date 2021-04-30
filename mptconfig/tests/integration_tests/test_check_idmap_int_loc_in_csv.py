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
    {
        "int_locs": {
            0: "OW760001",
            1: "OW760101",
            2: "OW760201",
            3: "OW760202",
            4: "OW760301",
            5: "KW760301",
            6: "OW760401",
            7: "OW760401",
            8: "OW760501",
            9: "OW760601",
            10: "OW760701",
            11: "OW760801",
            12: "OW760901",
            13: "OW761001",
            14: "OW761002",
            15: "KW761001",
            16: "OW761202",
            17: "OW761201",
            18: "KW761201",
            19: "KW4315xx",
            20: "KW4322xx",
            21: "OW760001",
            22: "OW760101",
            23: "OW760201",
            24: "OW760202",
            25: "OW760301",
            26: "KW760301",
            27: "OW760401",
            28: "OW760401",
            29: "OW760501",
            30: "OW760601",
            31: "OW760701",
            32: "OW760801",
            33: "OW760901",
            34: "OW761001",
            35: "OW761002",
            36: "KW761001",
            37: "OW761202",
            38: "OW761201",
            39: "KW761201",
        },
        "error_type": {
            0: "not in any csv",
            1: "not in any csv",
            2: "not in any csv",
            3: "not in any csv",
            4: "not in any csv",
            5: "not in any csv",
            6: "not in any csv",
            7: "not in any csv",
            8: "not in any csv",
            9: "not in any csv",
            10: "not in any csv",
            11: "not in any csv",
            12: "not in any csv",
            13: "not in any csv",
            14: "not in any csv",
            15: "not in any csv",
            16: "not in any csv",
            17: "not in any csv",
            18: "not in any csv",
            19: "not in any csv",
            20: "not in any csv",
            21: "not in any csv",
            22: "not in any csv",
            23: "not in any csv",
            24: "not in any csv",
            25: "not in any csv",
            26: "not in any csv",
            27: "not in any csv",
            28: "not in any csv",
            29: "not in any csv",
            30: "not in any csv",
            31: "not in any csv",
            32: "not in any csv",
            33: "not in any csv",
            34: "not in any csv",
            35: "not in any csv",
            36: "not in any csv",
            37: "not in any csv",
            38: "not in any csv",
            39: "not in any csv",
        },
    }
)


def test_check_idmap_int_loc_in_csv_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_idmap_int_loc_in_csv(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 40
    assert equal_dataframes(expected_df=expected_df_1_and_2, test_df=excelsheet.df)


def test_check_idmap_int_loc_in_csv_2(patched_path_constants_1):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_idmap_int_loc_in_csv(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 40
    assert equal_dataframes(expected_df=expected_df_1_and_2, test_df=excelsheet.df)
