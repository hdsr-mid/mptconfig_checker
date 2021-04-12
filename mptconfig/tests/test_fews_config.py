from mptconfig import constants
from mptconfig.checker import MptConfigChecker
from mptconfig.fews_utilities import FewsConfig
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from pathlib import Path

import mptconfig.tests.fixtures


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2


def test_fews_config_instance():
    path1 = mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_201902
    path2 = mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_202002
    fews_config1 = FewsConfig(path=path1)
    assert fews_config1.path == path1
    fews_config2 = FewsConfig(path=path2)
    assert fews_config2.path == path2
    for config in (fews_config1, fews_config2):
        for set_name, file in config.MapLayerFiles.items():
            assert isinstance(file, Path)


def test_fews_config_with_patched_paths_1(patched_path_constants_1, tmpdir):
    fews_config = FewsConfig(path=Path(tmpdir))
    assert fews_config.path == Path(tmpdir)
    checker = MptConfigChecker()
    assert checker.fews_config.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_201902


def test_fews_config_with_patched_paths_2(patched_path_constants_2, tmpdir):
    fews_config = FewsConfig(path=Path(tmpdir))
    assert fews_config.path == Path(tmpdir)
    checker = MptConfigChecker()
    assert checker.fews_config.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_202002
