from enum import Enum
from mptconfig.constants import BASE_DIR
from mptconfig.constants import check_constants_paths
from mptconfig.constants import PathConstants
from mptconfig.constants import PathNamedTuple
from pathlib import Path
from unittest.mock import patch

import logging
import pytest


logger = logging.getLogger(__name__)


TEST_DATA_DIR = BASE_DIR / "test" / "data"
ORIGINAL_PATH_CONSTANTS = PathConstants


@pytest.fixture(autouse=False)
def patched_path_constants_1():
    """Use context manager to patch constants.PathConstants. We patch since constants.PathConstants may
    change in the future while the test must use fixed paths (same test input every test run."""

    class PatchedPathConstants(Enum):
        result_xlsx = PathNamedTuple(
            is_file=True,
            should_exist=False,
            path=TEST_DATA_DIR / "output" / "result.xlsx",
            description="",
        )
        histtags_csv = PathNamedTuple(
            is_file=True,
            should_exist=True,
            description="",
            path=TEST_DATA_DIR / "input" / "get_series_startenddate_CAW_summary_total_sorted_20200930.csv",
        )
        fews_config = PathNamedTuple(
            is_file=False,
            should_exist=True,
            path=Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config",
            description="",
        )
        output_dir = PathNamedTuple(is_file=False, should_exist=False, path=TEST_DATA_DIR / "output", description="")
        ignored_ex_loc = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_ex_loc.csv",
            description="",
        )
        ignored_histtag = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_histtag.csv",
            description="",
        )
        ignored_ts800 = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_ts800.csv",
            description="",
        )
        ignored_xy = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_xy.csv",
            description="",
        )

    # https://chase-seibert.github.io/blog/2015/06/25/python-mocking-cookbook.html
    # The biggest mistake people make is mocking something out in the wrong place.
    # You always need to mock the thing where it’s imported TO, not where it’s imported FROM.
    # In other words: if you’re importing 'from foo import bar' into a package bat.baz,
    # you need to mock it as @mock.patch('bat.baz.bar')
    target = f"{__name__}.PathConstants"
    if not sorted(PatchedPathConstants.__members__) == sorted(PathConstants.__members__):
        raise AssertionError("PatchedPathConstants should have same members as the original PathConstants")
    logger.debug(f"patching {target}")
    with patch(target=target, new=PatchedPathConstants):
        yield


@pytest.fixture(autouse=False)
def patched_path_constants_2():
    """Use context manager to patch constants.PathConstants. We patch since constants.PathConstants may
    change in the future while the test must use fixed paths (same test input every test run."""

    class PatchedPathConstants(Enum):
        result_xlsx = PathNamedTuple(
            is_file=True,
            should_exist=False,
            path=TEST_DATA_DIR / "output" / "result.xlsx",
            description="",
        )
        histtags_csv = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
            description="",
        )
        fews_config = PathNamedTuple(
            is_file=False,
            should_exist=True,
            path=Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config",
            description="",
        )
        output_dir = PathNamedTuple(is_file=False, should_exist=False, path=TEST_DATA_DIR / "output", description="")
        ignored_ex_loc = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_ex_loc.csv",
            description="",
        )
        ignored_histtag = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_histtag.csv",
            description="",
        )
        ignored_ts800 = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_ts800.csv",
            description="",
        )
        ignored_xy = PathNamedTuple(
            is_file=True,
            should_exist=True,
            path=TEST_DATA_DIR / "input" / "ignored_xy.csv",
            description="",
        )

    target = f"{__name__}.PathConstants"
    if not sorted(PatchedPathConstants.__members__) == sorted(PathConstants.__members__):
        raise AssertionError("PatchedPathConstants should have same members as the original PathConstants")
    logger.debug(f"patching {target}")
    with patch(target=target, new=PatchedPathConstants):
        yield


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
