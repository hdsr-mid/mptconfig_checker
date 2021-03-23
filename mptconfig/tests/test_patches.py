from enum import Enum
from mptconfig.constants import BASE_DIR
from mptconfig.constants import PathConstants
from mptconfig.tests.patches import patched_path_constants_1
from mptconfig.tests.patches import patched_path_constants_2
from mptconfig.tests.patches import PatchedPathConstants1
from mptconfig.tests.patches import PatchedPathConstants2
from pathlib import Path


def test_members_patched_path_constants_1_and_2():
    """ensure that patched path constants has the same members as the original. """
    if not sorted(PatchedPathConstants1.__members__) == sorted(PathConstants.__members__):
        raise AssertionError(f"{PatchedPathConstants1.__name__} should have same members as original PathConstants")
    if not sorted(PatchedPathConstants2.__members__) == sorted(PathConstants.__members__):
        raise AssertionError(f"{PatchedPathConstants2.__name__} should have same members as original PathConstants")


def test_patched_constants1(patched_path_constants_1):
    original_paths = PathConstants
    from mptconfig.constants import PathConstants as new_paths

    isinstance(original_paths, Enum) and isinstance(new_paths, Enum)
    path1 = original_paths.fews_config.value.path
    path2 = new_paths.fews_config.value.path
    isinstance(path1, Path) and isinstance(path2, Path)
    assert (
        new_paths.fews_config.value.path
        == Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    )
    assert (
        new_paths.histtags_csv.value.path
        == BASE_DIR
        / "mptconfig"
        / "tests"
        / "data"
        / "input"
        / "get_series_startenddate_CAW_summary_total_sorted_20200930.csv"
    )


def test_patched_constants2(patched_path_constants_2):
    original_paths = PathConstants
    from mptconfig.constants import PathConstants as new_paths

    isinstance(original_paths, Enum) and isinstance(new_paths, Enum)
    path1 = original_paths.fews_config.value.path
    path2 = new_paths.fews_config.value.path
    isinstance(path1, Path) and isinstance(path2, Path)
    assert (
        new_paths.fews_config.value.path
        == Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    )
    assert (
        new_paths.histtags_csv.value.path
        == BASE_DIR
        / "mptconfig"
        / "tests"
        / "data"
        / "input"
        / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv"
    )


def test_path_constants_location():
    """almost all tests use a patched version of mptconfig.constants.PathConstants
    e.g. @p"""
    module_name = "mptconfig.constants"
    class_name = "PathConstants"
    _module = __import__(name=module_name, fromlist=[class_name])
    _class = getattr(_module, class_name)
    # TODO: activate this
    #  assert _class.__name__ == class_name
    assert 1 + 1 == 2
