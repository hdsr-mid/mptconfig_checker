from enum import Enum
from mptconfig.constants import BASE_DIR
from mptconfig.constants import D_DRIVE
from mptconfig.constants import PathNamedTuple
from pathlib import Path
from unittest.mock import patch

import logging
import pytest
import tempfile


logger = logging.getLogger(__name__)


TEST_DATA_DIR = BASE_DIR / "mptconfig" / "tests" / "data"
D_WIS_60_REFERENTIE_201902 = D_DRIVE / "WIS_6.0_REFERENTIE_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
D_WIS_60_REFERENTIE_202002 = D_DRIVE / "WIS_6.0_REFERENTIE_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
# we use a tempdir, so that all files that are created during test are deleted after a test run
TMP_OUTPUT_DIR = Path(tempfile.tempdir)

assert TEST_DATA_DIR.is_dir()


class PatchedPathConstants1(Enum):
    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=TMP_OUTPUT_DIR / "output" / "result.xlsx",
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
        path=D_WIS_60_REFERENTIE_201902,
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
    ignored_time_series_error = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=TEST_DATA_DIR / "input" / "ignored_time_series_error.csv",
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


class PatchedPathConstants2(Enum):
    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=TMP_OUTPUT_DIR / "output" / "result.xlsx",
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
        path=D_WIS_60_REFERENTIE_202002,
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
    ignored_time_series_error = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=TEST_DATA_DIR / "input" / "ignored_time_series_error.csv",
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


@pytest.fixture(autouse=False, scope="function")
def patched_path_constants_1():
    """Ideally we test with unit tests. Since we are in a hurry (and lack of time) we
    test now with integration tests. This means that we use a reference FEWS-config, that does not
    change over time. This means that the paths defined in "mptconfig.constants.PathConstants" are
    patched with paths to files/dirs of which the content does not change over time (PatchedPathConstants1)."""
    target = "mptconfig.constants.PathConstants"
    logger.debug(f"patching {target}")
    with patch(target=target, new=PatchedPathConstants1) as patched:
        yield patched


@pytest.fixture(autouse=False, scope="function")
def patched_path_constants_2():
    """Ideally we test with unit tests. Since we are in a hurry (and lack of time) we
    test now with integration tests. This means that we use a reference FEWS-config, that does not
    change over time. This means that the paths defined in "mptconfig.constants.PathConstants" are
    patched with paths to files/dirs of which the content does not change over time (PatchedPathConstants2)."""
    target = "mptconfig.constants.PathConstants"
    logger.debug(f"patching {target}")
    with patch(target=target, new=PatchedPathConstants2) as patched:
        yield patched
