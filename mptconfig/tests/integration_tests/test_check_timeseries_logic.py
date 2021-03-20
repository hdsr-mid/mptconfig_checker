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
        "internalLocation": {
            0: "KW106112",
            1: "KW218613",
            2: "KW218614",
            3: "KW218619",
            4: "KW323515",
            5: "KW324813",
            6: "KW435013",
        },
        "eind": {
            0: pd.Timestamp("2100-01-01 00:00:00"),
            1: pd.Timestamp("2100-01-01 00:00:00"),
            2: pd.Timestamp("2100-01-01 00:00:00"),
            3: pd.Timestamp("2100-01-01 00:00:00"),
            4: pd.Timestamp("2100-01-01 00:00:00"),
            5: pd.Timestamp("2100-01-01 00:00:00"),
            6: pd.Timestamp("2100-01-01 00:00:00"),
        },
        "internalParameters": {
            0: "Q.G.0",
            1: "ES.0,POS.0",
            2: "ES.0,POS.0",
            3: "ES.0,POS.0,Q.G.0",
            4: "POS.0,Q.G.0",
            5: "DD.15,IB.0",
            6: "ES.0,POS.0,Q.G.0",
        },
        "externalParameters": {
            0: "Q2",
            1: "ES1,SP1",
            2: "ES2,SP2",
            3: "ES3,Q4,SP5",
            4: "Q4,SP1",
            5: "I2B,IB2",
            6: "ES1,Q2,SP1",
        },
        "externalLocations": {
            0: "1061",
            1: "186,2186",
            2: "186,2186",
            3: "2186",
            4: "235,3235",
            5: "248,3248",
            6: "350,4350",
        },
        "type": {0: "overlaat", 1: "afsluiter", 2: "afsluiter", 3: "schuif", 4: "schuif", 5: "pompvijzel", 6: "schuif"},
        "fout": {
            0: "overlaat zonder stuurpeil KW106111 wel",
            1: "afsluiter zonder stuurpeil KW218611,KW218612 wel",
            2: "afsluiter zonder stuurpeil KW218611,KW218612 wel",
            3: "schuif zonder stuurpeil KW218611,KW218612 wel",
            4: "schuif zonder stuurpeil KW323513,KW323514 wel",
            5: "pompvijzel zonder stuurpeil KW324812 wel",
            6: "schuif zonder stuurpeil KW435012 wel",
        },
    }
)


def test_check_timeseries_logic_1(patched_path_constants_1):
    """integration test with patched paths 1"""
    from mptconfig.constants import PathConstants
    from pathlib import Path

    assert (
        PathConstants.fews_config.value.path
        == Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    )
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_timeseries_logic(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 7
    ensure_dataframes_equal(expected_df=expected_df_1_and_2, test_df=excelsheet.df)


def test_check_timeseries_logic_2(patched_path_constants_2):
    """integration test with patched paths 2"""
    from mptconfig.constants import PathConstants
    from pathlib import Path

    assert (
        PathConstants.fews_config.value.path
        == Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    )
    meetpunt_config = MptConfigChecker()
    excelsheet = meetpunt_config.check_timeseries_logic(sheet_name="blabla")
    assert isinstance(excelsheet, ExcelSheet)
    assert excelsheet.name == "blabla"
    assert excelsheet.sheet_type == ExcelSheetTypeChoices.output_check
    assert excelsheet.nr_rows == 7
    ensure_dataframes_equal(expected_df=expected_df_1_and_2, test_df=excelsheet.df)
