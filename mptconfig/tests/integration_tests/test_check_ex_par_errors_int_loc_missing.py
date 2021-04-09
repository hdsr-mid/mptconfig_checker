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


expected_df_int_loc_1 = pd.DataFrame({"internalLocation": {0: "KW4315xx", 1: "KW4322xx"}})

expected_df_ex_par_1 = pd.DataFrame(
    {
        "internalLocation": {
            0: "KW101011",
            1: "KW109711",
            2: "KW216013",
            3: "KW217311",
            4: "KW218221",
            5: "KW218231",
            6: "KW323016",
            7: "KW439711",
            8: "KW440811",
            9: "KW440812",
        },
        "locationType": {
            0: "subloc",
            1: "subloc",
            2: "subloc",
            3: "subloc",
            4: "subloc",
            5: "subloc",
            6: "subloc",
            7: "subloc",
            8: "subloc",
            9: "subloc",
        },
        "ex_par_error": {0: "", 1: "", 2: "", 3: "", 4: "Q1", 5: "Q2", 6: "", 7: "", 8: "", 9: ""},
        "types": {
            0: "schuif,stuw,vispassage",
            1: "krooshek,pompvijzel",
            2: "krooshek,pompvijzel,schuif",
            3: "schuif",
            4: "afsluiter",
            5: "afsluiter",
            6: "krooshek,pompvijzel,schuif,totaal,vispassage",
            7: "pompvijzel",
            8: "krooshek,pompvijzel,stuw,totaal,vispassage",
            9: "krooshek,pompvijzel,stuw,totaal,vispassage",
        },
        "FQ": {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False},
        "I.X": {0: False, 1: True, 2: False, 3: False, 4: False, 5: False, 6: False, 7: True, 8: True, 9: True},
        "IX.": {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False, 9: False},
        "SS./SM.": {0: True, 1: False, 2: True, 3: True, 4: False, 5: False, 6: True, 7: False, 8: False, 9: False},
    }
)

expected_df_ex_par_2 = pd.DataFrame(
    {
        "internalLocation": {
            0: "KW101011",
            1: "KW216013",
            2: "KW217311",
            3: "KW218221",
            4: "KW218231",
            5: "KW440811",
            6: "KW440812",
        },
        "locationType": {0: "subloc", 1: "subloc", 2: "subloc", 3: "subloc", 4: "subloc", 5: "subloc", 6: "subloc"},
        "ex_par_error": {0: "", 1: "", 2: "", 3: "Q1", 4: "Q2", 5: "", 6: ""},
        "types": {
            0: "schuif,stuw,vispassage",
            1: "krooshek,pompvijzel,schuif",
            2: "schuif",
            3: "afsluiter",
            4: "afsluiter",
            5: "krooshek,pompvijzel,stuw,totaal,vispassage",
            6: "krooshek,pompvijzel,stuw,totaal,vispassage",
        },
        "FQ": {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False},
        "I.X": {0: False, 1: False, 2: False, 3: False, 4: False, 5: True, 6: True},
        "IX.": {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False},
        "SS./SM.": {0: True, 1: True, 2: True, 3: False, 4: False, 5: False, 6: False},
    }
)


def test_check_ex_par_errors_int_loc_missing_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    ex_par_sheet, int_loc_sheet = meetpunt_config.check_ex_par_errors_int_loc_missing(
        ex_par_sheet_name="blaat1", int_loc_sheet_name="blaat2"
    )
    assert isinstance(ex_par_sheet, ExcelSheet) and isinstance(int_loc_sheet, ExcelSheet)
    assert ex_par_sheet.name == "blaat1" and int_loc_sheet.name == "blaat2"
    assert (ex_par_sheet.sheet_type and int_loc_sheet.sheet_type) == ExcelSheetTypeChoices.output_check
    assert ex_par_sheet.nr_rows == 10
    assert int_loc_sheet.nr_rows == 2
    assert equal_dataframes(expected_df=expected_df_ex_par_1, test_df=ex_par_sheet.df)
    assert equal_dataframes(expected_df=expected_df_int_loc_1, test_df=int_loc_sheet.df)


def test_check_ex_par_errors_int_loc_missing_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    ex_par_sheet, int_loc_sheet = meetpunt_config.check_ex_par_errors_int_loc_missing(
        ex_par_sheet_name="blaat1", int_loc_sheet_name="blaat2"
    )
    assert isinstance(ex_par_sheet, ExcelSheet) and isinstance(int_loc_sheet, ExcelSheet)
    assert ex_par_sheet.name == "blaat1" and int_loc_sheet.name == "blaat2"
    assert (ex_par_sheet.sheet_type and int_loc_sheet.sheet_type) == ExcelSheetTypeChoices.output_check
    assert ex_par_sheet.nr_rows == 7
    assert int_loc_sheet.nr_rows == 0
    assert equal_dataframes(expected_df=expected_df_ex_par_2, test_df=ex_par_sheet.df)
