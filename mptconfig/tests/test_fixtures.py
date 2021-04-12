from enum import Enum
from enum import EnumMeta
from mptconfig import constants
from mptconfig.constants import BASE_DIR
from mptconfig.constants import PathConstants
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from mptconfig.tests.fixtures import PatchedPathConstants1
from mptconfig.tests.fixtures import PatchedPathConstants2
from pathlib import Path

import mptconfig.tests.fixtures


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


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
    assert new_paths.fews_config.value.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_201902
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
    assert new_paths.fews_config.value.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_202002
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
    """
    fixtures patched_path_constants_1 and patched_path_constants_2 patch location 'mptconfig.constants.PathConstants'.
    Ensure that this location exists, and that it is a Enum class.
    """
    module_name = "mptconfig.constants"
    class_name = "PathConstants"
    _module = __import__(name=module_name, fromlist=[class_name])
    assert getattr(_module, class_name), f"class {module_name}.{class_name} should exists. This is patched in fixtures"
    assert isinstance(getattr(_module, class_name), EnumMeta), "PathConstants should be a EnumMeta"
