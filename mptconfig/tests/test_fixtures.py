from mptconfig.constants import check_constants_paths
from mptconfig.constants import PathConstants
from mptconfig.tests.fixtures import ORIGINAL_PATH_CONSTANTS
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from mptconfig.tests.fixtures import TEST_DATA_DIR
from pathlib import Path


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


def test_ensure_patched_path_constants_1_works(patched_path_constants_1):
    original_fews_config_path = ORIGINAL_PATH_CONSTANTS.fews_config.value.path
    patched_fews_config_path = PathConstants.fews_config.value.path
    assert isinstance(original_fews_config_path, Path) and isinstance(patched_fews_config_path, Path)
    assert original_fews_config_path != patched_fews_config_path
    assert (
        patched_fews_config_path == Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    )
    assert (
        PathConstants.histtags_csv.value.path
        == TEST_DATA_DIR / "input" / "get_series_startenddate_CAW_summary_total_sorted_20200930.csv"
    )
    # check all patched constant paths
    check_constants_paths()


def test_ensure_patched_path_constants_2_works(patched_path_constants_2):
    original_fews_config_path = ORIGINAL_PATH_CONSTANTS.fews_config.value.path
    patched_fews_config_path = PathConstants.fews_config.value.path
    assert isinstance(original_fews_config_path, Path) and isinstance(patched_fews_config_path, Path)
    assert original_fews_config_path != patched_fews_config_path
    assert (
        patched_fews_config_path == Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    )
    assert (
        PathConstants.histtags_csv.value.path
        == TEST_DATA_DIR / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv"
    )
    # check all patched constant paths
    check_constants_paths()
