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


expected_df_1_and_2 = pd.DataFrame(
    {
        "LOC_ID": {
            0: "KW100110",
            1: "KW100410",
            2: "KW110210",
            3: "KW210310",
            4: "KW214610",
            5: "KW215310",
            6: "KW217710",
            7: "KW218310",
            8: "KW431110",
            9: "KW431610",
            10: "KW432010",
            11: "KW432110",
            12: "KW433130",
            13: "KW435010",
            14: "KW436410",
            15: "KW436810",
            16: "KW437010",
            17: "KW440710",
        },
        "SUB_LOCS": {
            0: "KW100111,KW100112",
            1: "KW100411,KW100412,KW100413,KW100414,KW100415",
            2: "KW110211,KW110212",
            3: "KW210311,KW210312,KW210313,KW210314,KW210315,KW210316",
            4: "KW214611,KW214612,KW214613,KW214614,KW214615,KW214616,KW214617,KW214618,KW214619",
            5: "KW215311,KW215312,KW215313,KW215314",
            6: "KW217711,KW217712",
            7: "KW218311,KW218312",
            8: "KW431111,KW431112,KW431113,KW431114,KW431115",
            9: "KW431611,KW431612",
            10: "KW432011,KW432012,KW432013",
            11: "KW432111,KW432112,KW432113",
            12: "KW433131,KW433132,KW433133",
            13: "KW435011,KW435012,KW435013,KW435014",
            14: "KW436411,KW436412,KW436413,KW436414,KW436415,KW436416,KW436417",
            15: "KW436811,KW436812,KW436813,KW436814,KW436815",
            16: "KW437011,KW437012,KW437013,KW437014,KW437015,KW437016,KW437017",
            17: "KW440711,KW440712,KW440713,KW440714,KW440715",
        },
        "LOC_NAME": {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
            11: "",
            12: "",
            13: "",
            14: "",
            15: "",
            16: "",
            17: "",
        },
        "GEOMETRY": {
            0: "(150502.0 442988.0),(150501.0 442986.0)",
            1: "",
            2: "(139919.0 444295.0),(139917.0 444289.0)",
            3: "(126558.0 455645.0),(126556.0 455654.0)",
            4: "(135733.0 451465.0),(135734.0 451468.0)",
            5: "(133415.0 459463.0),(133415.0 459464.0),(133416.0 459462.0)",
            6: "(126306.0 462676.0),(126307.0 462675.0)",
            7: "(132256.0 458598.0),(132256.0 458599.0)",
            8: "(119378.0 462409.0),(119381.0 462412.0)",
            9: "(120901.0 463972.0),(120903.0 463975.0)",
            10: "(124376.0 458319.0),(124374.0 458318.0)",
            11: "(115778.0 455797.0),(115779.0 455799.0)",
            12: "(113797.0 456151.0),(113807.0 456144.0)",
            13: "(123072.0 453206.0),(123069.0 453200.0)",
            14: "(120070.0 453779.0),(120056.0 453761.0)",
            15: "(121293.0 455149.0),(119302.0 455149.0)",
            16: "(113543.0 450564.0),(113529.0 450558.0)",
            17: "(121452.0 448936.0),(121454.0 448938.0)",
        },
        "SYSTEEM": {
            0: "",
            1: "AMSTERDAM RIJN KANAAL,",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
            11: "",
            12: "",
            13: "",
            14: "",
            15: "",
            16: "",
            17: "",
        },
        "RAYON": {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
            11: "",
            12: "",
            13: "",
            14: "",
            15: "",
            16: "",
            17: "",
        },
        "KOMPAS": {
            0: "",
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
            11: "",
            12: "",
            13: "",
            14: "",
            15: "",
            16: "",
            17: "",
        },
    }
)


def test_check_h_loc_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_h_loc(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 18
    ensure_dataframes_equal(expected_df=expected_df_1_and_2, test_df=excelsheet.df)


def test_check_h_loc_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_h_loc(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 18
    ensure_dataframes_equal(expected_df=expected_df_1_and_2, test_df=excelsheet.df)
