from mptconfig.checker import MptConfigChecker
from mptconfig.constants import PathConstants
from mptconfig.fews_utilities import FewsConfig
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from pathlib import Path


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


def test_fews_config_instance():
    path1 = Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    path2 = Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    a = FewsConfig(path=path1)
    assert a.path == path1
    b = FewsConfig(path=path2)
    assert b.path == path2
    for config in (a, b):
        for set_name, file in config.MapLayerFiles.items():
            assert isinstance(file, Path)


def test_fews_config_with_patched_paths_1(patched_path_constants_1, tmpdir):
    from mptconfig.constants import PathConstants

    expected_path = Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    assert PathConstants.fews_config.value.path == expected_path
    # FewsConfig path is set during loading application (so not affected by patched paths)
    fews_config = FewsConfig(path=Path(tmpdir))
    assert fews_config.path == Path(tmpdir)
    # MptConfigChecker path is not set during loading application (so affected by patched paths)
    checker = MptConfigChecker()
    assert checker.fews_config.path == expected_path


def test_fews_config_with_patched_paths_2(patched_path_constants_2, tmpdir):
    expected_path = Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    from mptconfig.constants import PathConstants

    assert PathConstants.fews_config.value.path == expected_path
    # FewsConfig path is set during loading application (so not affected by patched paths)
    fews_config = FewsConfig(path=Path(tmpdir))
    assert fews_config.path == Path(tmpdir)
    # MptConfigChecker path is not set during loading application (so affected by patched paths)
    checker = MptConfigChecker()
    assert checker.fews_config.path == expected_path
