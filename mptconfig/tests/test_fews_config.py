from mptconfig.fews_utilities import FewsConfig
from pathlib import Path


def test_ensure_fews_config_singleton():
    path1 = Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    path2 = Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config"
    a = FewsConfig(path=path1)
    assert a.path == path1
    b = FewsConfig(path=path2)
    assert b.path == path2
    for config in (a, b):
        for set_name, file in config.MapLayerFiles.items():
            assert isinstance(file, Path)
