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
            0: "KW100712",
            1: "KW101011",
            2: "KW101611",
            3: "KW103212",
            4: "KW103512",
            5: "KW104511",
            6: "KW104611",
            7: "KW104912",
            8: "KW105111",
            9: "KW105411",
            10: "KW105811",
            11: "KW106013",
            12: "KW106111",
            13: "KW106311",
            14: "KW107211",
            15: "KW107311",
            16: "KW107411",
            17: "KW107611",
            18: "KW107811",
            19: "KW108111",
            20: "KW108411",
            21: "KW108421",
            22: "KW109511",
            23: "KW109711",
            24: "KW110111",
            25: "KW210111",
            26: "KW210211",
            27: "KW210811",
            28: "KW210912",
            29: "KW211211",
            30: "KW211312",
            31: "KW211412",
            32: "KW211711",
            33: "KW211911",
            34: "KW214811",
            35: "KW214911",
            36: "KW215012",
            37: "KW215811",
            38: "KW215911",
            39: "KW216013",
            40: "KW216311",
            41: "KW216811",
            42: "KW216911",
            43: "KW217211",
            44: "KW217311",
            45: "KW217711",
            46: "KW218111",
            47: "KW218221",
            48: "KW218231",
            49: "KW320311",
            50: "KW322612",
            51: "KW322711",
            52: "KW323016",
            53: "KW323111",
            54: "KW323211",
            55: "KW323311",
            56: "KW323811",
            57: "KW324111",
            58: "KW324211",
            59: "KW324411",
            60: "KW324611",
            61: "KW324621",
            62: "KW324711",
            63: "KW431911",
            64: "KW433611",
            65: "KW437913",
            66: "KW438711",
            67: "KW439711",
            68: "KW440511",
            69: "KW440811",
            70: "KW440812",
            71: "KW446911",
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
            10: "subloc",
            11: "subloc",
            12: "subloc",
            13: "subloc",
            14: "subloc",
            15: "subloc",
            16: "subloc",
            17: "subloc",
            18: "subloc",
            19: "subloc",
            20: "subloc",
            21: "subloc",
            22: "subloc",
            23: "subloc",
            24: "subloc",
            25: "subloc",
            26: "subloc",
            27: "subloc",
            28: "subloc",
            29: "subloc",
            30: "subloc",
            31: "subloc",
            32: "subloc",
            33: "subloc",
            34: "subloc",
            35: "subloc",
            36: "subloc",
            37: "subloc",
            38: "subloc",
            39: "subloc",
            40: "subloc",
            41: "subloc",
            42: "subloc",
            43: "subloc",
            44: "subloc",
            45: "subloc",
            46: "subloc",
            47: "subloc",
            48: "subloc",
            49: "subloc",
            50: "subloc",
            51: "subloc",
            52: "subloc",
            53: "subloc",
            54: "subloc",
            55: "subloc",
            56: "subloc",
            57: "subloc",
            58: "subloc",
            59: "subloc",
            60: "subloc",
            61: "subloc",
            62: "subloc",
            63: "subloc",
            64: "subloc",
            65: "subloc",
            66: "subloc",
            67: "subloc",
            68: "subloc",
            69: "subloc",
            70: "subloc",
            71: "subloc",
        },
        "ex_par_error": {
            0: "ES1",
            1: "",
            2: "ES1",
            3: "ES1",
            4: "ES1",
            5: "ES1",
            6: "ES1",
            7: "ES1",
            8: "ES1",
            9: "ES1",
            10: "ES1",
            11: "ES1",
            12: "ES1",
            13: "ES1",
            14: "ES1",
            15: "ES1",
            16: "ES1",
            17: "ES1",
            18: "ES1",
            19: "ES1",
            20: "ES1",
            21: "ES2",
            22: "ES1",
            23: "",
            24: "ES1",
            25: "ES1",
            26: "ES1",
            27: "ES1",
            28: "ES1",
            29: "ES1",
            30: "ES1",
            31: "ES1",
            32: "ES1",
            33: "ES1",
            34: "ES1",
            35: "ES1",
            36: "ES1",
            37: "ES1",
            38: "ES1",
            39: "",
            40: "ES1",
            41: "ES1",
            42: "ES1",
            43: "ES1",
            44: "",
            45: "ES1",
            46: "ES1",
            47: "Q1",
            48: "Q2",
            49: "ES1",
            50: "ES1",
            51: "ES1",
            52: "",
            53: "ES1",
            54: "ES1",
            55: "ES1",
            56: "ES1",
            57: "ES1",
            58: "ES1",
            59: "ES1",
            60: "ES1",
            61: "ES2",
            62: "ES1",
            63: "ES1",
            64: "ES1",
            65: "ES1",
            66: "ES1",
            67: "",
            68: "ES1",
            69: "",
            70: "",
            71: "ES1",
        },
        "types": {
            0: "pompvijzel,stuw,totaal",
            1: "schuif,stuw,vispassage",
            2: "stuw",
            3: "pompvijzel,stuw,totaal",
            4: "pompvijzel,stuw,totaal",
            5: "stuw",
            6: "stuw",
            7: "krooshek,stuw",
            8: "stuw",
            9: "stuw",
            10: "stuw",
            11: "krooshek,pompvijzel,stuw,totaal",
            12: "stuw,overlaat,totaal",
            13: "stuw",
            14: "stuw",
            15: "stuw",
            16: "stuw",
            17: "stuw",
            18: "stuw",
            19: "stuw",
            20: "stuw",
            21: "stuw",
            22: "stuw",
            23: "krooshek,pompvijzel",
            24: "stuw",
            25: "stuw",
            26: "stuw",
            27: "stuw",
            28: "pompvijzel,stuw,totaal",
            29: "stuw",
            30: "pompvijzel,stuw,totaal",
            31: "pompvijzel,stuw,totaal",
            32: "stuw",
            33: "stuw",
            34: "stuw",
            35: "stuw",
            36: "pompvijzel,stuw,totaal",
            37: "stuw",
            38: "stuw",
            39: "krooshek,pompvijzel,schuif",
            40: "stuw",
            41: "stuw",
            42: "stuw",
            43: "stuw",
            44: "schuif",
            45: "pompvijzel,stuw",
            46: "stuw",
            47: "afsluiter",
            48: "afsluiter",
            49: "stuw",
            50: "pompvijzel,stuw,totaal",
            51: "stuw",
            52: "krooshek,pompvijzel,schuif,totaal,vispassage",
            53: "stuw",
            54: "stuw",
            55: "stuw",
            56: "stuw",
            57: "stuw",
            58: "stuw",
            59: "stuw",
            60: "stuw",
            61: "stuw",
            62: "stuw",
            63: "stuw",
            64: "stuw",
            65: "krooshek,pompvijzel,stuw,totaal",
            66: "stuw",
            67: "pompvijzel",
            68: "stuw",
            69: "krooshek,pompvijzel,stuw,totaal,vispassage",
            70: "krooshek,pompvijzel,stuw,totaal,vispassage",
            71: "stuw",
        },
        "FQ": {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
            69: False,
            70: False,
            71: False,
        },
        "I.X": {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: True,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: True,
            68: False,
            69: True,
            70: True,
            71: False,
        },
        "IX.": {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
            69: False,
            70: False,
            71: False,
        },
        "SS./SM.": {
            0: False,
            1: True,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: True,
            40: False,
            41: False,
            42: False,
            43: False,
            44: True,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: True,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
            69: False,
            70: False,
            71: False,
        },
    }
)

expected_df_ex_par_2 = pd.DataFrame(
    {
        "internalLocation": {
            0: "KW100712",
            1: "KW101011",
            2: "KW101611",
            3: "KW103212",
            4: "KW103512",
            5: "KW104511",
            6: "KW104611",
            7: "KW104912",
            8: "KW105111",
            9: "KW105411",
            10: "KW105811",
            11: "KW106013",
            12: "KW106111",
            13: "KW106311",
            14: "KW107211",
            15: "KW107311",
            16: "KW107411",
            17: "KW107611",
            18: "KW107811",
            19: "KW108111",
            20: "KW108411",
            21: "KW108421",
            22: "KW109511",
            23: "KW110111",
            24: "KW210111",
            25: "KW210211",
            26: "KW210811",
            27: "KW210912",
            28: "KW211211",
            29: "KW211312",
            30: "KW211412",
            31: "KW211711",
            32: "KW211911",
            33: "KW214811",
            34: "KW214911",
            35: "KW215012",
            36: "KW215811",
            37: "KW215911",
            38: "KW216013",
            39: "KW216311",
            40: "KW216811",
            41: "KW216911",
            42: "KW217211",
            43: "KW217311",
            44: "KW217711",
            45: "KW218111",
            46: "KW218221",
            47: "KW218231",
            48: "KW320311",
            49: "KW322612",
            50: "KW322711",
            51: "KW323111",
            52: "KW323211",
            53: "KW323311",
            54: "KW323811",
            55: "KW324111",
            56: "KW324211",
            57: "KW324411",
            58: "KW324611",
            59: "KW324621",
            60: "KW324711",
            61: "KW431911",
            62: "KW433611",
            63: "KW437913",
            64: "KW438711",
            65: "KW440511",
            66: "KW440811",
            67: "KW440812",
            68: "KW446911",
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
            10: "subloc",
            11: "subloc",
            12: "subloc",
            13: "subloc",
            14: "subloc",
            15: "subloc",
            16: "subloc",
            17: "subloc",
            18: "subloc",
            19: "subloc",
            20: "subloc",
            21: "subloc",
            22: "subloc",
            23: "subloc",
            24: "subloc",
            25: "subloc",
            26: "subloc",
            27: "subloc",
            28: "subloc",
            29: "subloc",
            30: "subloc",
            31: "subloc",
            32: "subloc",
            33: "subloc",
            34: "subloc",
            35: "subloc",
            36: "subloc",
            37: "subloc",
            38: "subloc",
            39: "subloc",
            40: "subloc",
            41: "subloc",
            42: "subloc",
            43: "subloc",
            44: "subloc",
            45: "subloc",
            46: "subloc",
            47: "subloc",
            48: "subloc",
            49: "subloc",
            50: "subloc",
            51: "subloc",
            52: "subloc",
            53: "subloc",
            54: "subloc",
            55: "subloc",
            56: "subloc",
            57: "subloc",
            58: "subloc",
            59: "subloc",
            60: "subloc",
            61: "subloc",
            62: "subloc",
            63: "subloc",
            64: "subloc",
            65: "subloc",
            66: "subloc",
            67: "subloc",
            68: "subloc",
        },
        "ex_par_error": {
            0: "ES1",
            1: "",
            2: "ES1",
            3: "ES1",
            4: "ES1",
            5: "ES1",
            6: "ES1",
            7: "ES1",
            8: "ES1",
            9: "ES1",
            10: "ES1",
            11: "ES1",
            12: "ES1",
            13: "ES1",
            14: "ES1",
            15: "ES1",
            16: "ES1",
            17: "ES1",
            18: "ES1",
            19: "ES1",
            20: "ES1",
            21: "ES2",
            22: "ES1",
            23: "ES1",
            24: "ES1",
            25: "ES1",
            26: "ES1",
            27: "ES1",
            28: "ES1",
            29: "ES1",
            30: "ES1",
            31: "ES1",
            32: "ES1",
            33: "ES1",
            34: "ES1",
            35: "ES1",
            36: "ES1",
            37: "ES1",
            38: "",
            39: "ES1",
            40: "ES1",
            41: "ES1",
            42: "ES1",
            43: "",
            44: "ES1",
            45: "ES1",
            46: "Q1",
            47: "Q2",
            48: "ES1",
            49: "ES1",
            50: "ES1",
            51: "ES1",
            52: "ES1",
            53: "ES1",
            54: "ES1",
            55: "ES1",
            56: "ES1",
            57: "ES1",
            58: "ES1",
            59: "ES2",
            60: "ES1",
            61: "ES1",
            62: "ES1",
            63: "ES1",
            64: "ES1",
            65: "ES1",
            66: "",
            67: "",
            68: "ES1",
        },
        "types": {
            0: "pompvijzel,stuw,totaal",
            1: "schuif,stuw,vispassage",
            2: "stuw",
            3: "pompvijzel,stuw,totaal",
            4: "pompvijzel,stuw,totaal",
            5: "stuw",
            6: "stuw",
            7: "krooshek,stuw",
            8: "stuw",
            9: "stuw",
            10: "stuw",
            11: "krooshek,pompvijzel,stuw,totaal",
            12: "stuw,overlaat,totaal",
            13: "stuw",
            14: "stuw",
            15: "stuw",
            16: "stuw",
            17: "stuw",
            18: "stuw",
            19: "stuw",
            20: "stuw",
            21: "stuw",
            22: "stuw",
            23: "stuw",
            24: "stuw",
            25: "stuw",
            26: "stuw",
            27: "pompvijzel,stuw,totaal",
            28: "stuw",
            29: "pompvijzel,stuw,totaal",
            30: "pompvijzel,stuw,totaal",
            31: "stuw",
            32: "stuw",
            33: "stuw",
            34: "stuw",
            35: "pompvijzel,stuw,totaal",
            36: "stuw",
            37: "stuw",
            38: "krooshek,pompvijzel,schuif",
            39: "stuw",
            40: "stuw",
            41: "stuw",
            42: "stuw",
            43: "schuif",
            44: "pompvijzel,stuw",
            45: "stuw",
            46: "afsluiter",
            47: "afsluiter",
            48: "stuw",
            49: "pompvijzel,stuw,totaal",
            50: "stuw",
            51: "stuw",
            52: "stuw",
            53: "stuw",
            54: "stuw",
            55: "stuw",
            56: "stuw",
            57: "stuw",
            58: "stuw",
            59: "stuw",
            60: "stuw",
            61: "stuw",
            62: "stuw",
            63: "krooshek,pompvijzel,stuw,totaal",
            64: "stuw",
            65: "stuw",
            66: "krooshek,pompvijzel,stuw,totaal,vispassage",
            67: "krooshek,pompvijzel,stuw,totaal,vispassage",
            68: "stuw",
        },
        "FQ": {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
        },
        "I.X": {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: True,
            67: True,
            68: False,
        },
        "IX.": {
            0: False,
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: False,
            39: False,
            40: False,
            41: False,
            42: False,
            43: False,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
        },
        "SS./SM.": {
            0: False,
            1: True,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False,
            8: False,
            9: False,
            10: False,
            11: False,
            12: False,
            13: False,
            14: False,
            15: False,
            16: False,
            17: False,
            18: False,
            19: False,
            20: False,
            21: False,
            22: False,
            23: False,
            24: False,
            25: False,
            26: False,
            27: False,
            28: False,
            29: False,
            30: False,
            31: False,
            32: False,
            33: False,
            34: False,
            35: False,
            36: False,
            37: False,
            38: True,
            39: False,
            40: False,
            41: False,
            42: False,
            43: True,
            44: False,
            45: False,
            46: False,
            47: False,
            48: False,
            49: False,
            50: False,
            51: False,
            52: False,
            53: False,
            54: False,
            55: False,
            56: False,
            57: False,
            58: False,
            59: False,
            60: False,
            61: False,
            62: False,
            63: False,
            64: False,
            65: False,
            66: False,
            67: False,
            68: False,
        },
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
    assert ex_par_sheet.nr_rows == 72
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
    assert ex_par_sheet.nr_rows == 69
    assert int_loc_sheet.nr_rows == 0
    assert equal_dataframes(expected_df=expected_df_ex_par_2, test_df=ex_par_sheet.df)
