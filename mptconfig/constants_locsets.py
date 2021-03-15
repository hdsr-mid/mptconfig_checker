from mptconfig.fews_utilities import FewsConfig
from typing import Dict
from typing import List

import mptconfig.constants_paths


class LocationSet:
    def __init__(self, name: str, fews_name: str, checker_property_name: str, validation_rules: List[Dict]):
        self.name = name
        self.fews_name = fews_name
        self.checker_property_name = checker_property_name
        self.validation_rules = validation_rules
        self._fews_config = None
        self._data = None

    @property
    def fews_config(self) -> FewsConfig:
        if self._fews_config is not None:
            return self._fews_config
        self._fews_config = FewsConfig(path=mptconfig.constants_paths.PathConstants.fews_config.path)
        return self._fews_config

    @property
    def data(self):
        if self._data is not None:
            return self._data
        location_set = self.fews_config.location_sets[self.fews_name]
        assert location_set["csvFile"], f"{self.name} data must have csvFile"
        self._data = self.fews_config.get_locations(location_set_key=self.fews_name)
        return self._data


hoofdloc = LocationSet(
    name="hoofdlocaties",
    fews_name="OPVLWATER_HOOFDLOC",
    checker_property_name="hoofdloc",
    validation_rules=[
        {"parameter": "H.S.", "extreme_values": {"hmax": "HS1_HMAX", "hmin": "HS1_HMIN"}},
        {"parameter": "H2.S.", "extreme_values": {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}},
        {"parameter": "H3.S.", "extreme_values": {"hmax": "HS3_HMAX", "hmin": "HS3_HMIN"}},
    ],
)

subloc = LocationSet(
    name="sublocaties",
    fews_name="OPVLWATER_SUBLOC",
    checker_property_name="subloc",
    validation_rules=[
        {"parameter": "H.R.", "extreme_values": {"hmax": "HR1_HMAX", "hmin": "HR1_HMIN"}},
        {"parameter": "H2.R.", "extreme_values": {"hmax": "HR2_HMAX", "hmin": "HR2_HMIN"}},
        {"parameter": "H3.R.", "extreme_values": {"hmax": "HR3_HMAX", "hmin": "HR3_HMIN"}},
        {
            "parameter": "Q.B.",
            "type": "debietmeter",
            "extreme_values": {"hmax": "Q_HMAX", "smax": "Q_SMAX", "smin": "Q_SMIN", "hmin": "Q_HMIN"},
        },
        {
            "parameter": "Q.G.",
            "type": "debietmeter",
            "extreme_values": {"hmax": "Q_HMAX", "smax": "Q_SMAX", "smin": "Q_SMIN", "hmin": "Q_HMIN"},
        },
        {"parameter": "F.", "extreme_values": {"hmax": "FRQ_HMAX", "hmin": "FRQ_HMIN"}},
        {"parameter": "Hh.", "extreme_values": {"hmax": "HEF_HMAX", "hmin": "HEF_HMIN"}},
        {
            "parameter": "POS.",
            "extreme_values": {"hmax": "PERC_HMAX", "smax": "PERC_SMAX", "smin": "PERC_SMIN", "hmin": "PERC_HMIN"},
        },
        {
            "parameter": "POS2.",
            "extreme_values": {"hmax": "PERC2_HMAX", "smax": "PERC2_SMAX", "smin": "PERC2_SMIN", "hmin": "PERC2_HMIN"},
        },
        {"parameter": "TT.", "extreme_values": {"hmax": "TT_HMAX", "hmin": "TT_HMIN"}},
    ],
)

waterstandloc = LocationSet(
    name="waterstandlocaties",
    fews_name="OPVLWATER_WATERSTANDEN_AUTO",
    checker_property_name="waterstandloc",
    validation_rules=[
        {
            "parameter": "H.G.",
            "extreme_values": {
                "hmax": "HARDMAX",
                "smax": [
                    {"period": 1, "attribute": "WIN_SMAX"},
                    {"period": 2, "attribute": "OV_SMAX"},
                    {"period": 3, "attribute": "ZOM_SMAX"},
                ],
                "smin": [
                    {"period": 1, "attribute": "WIN_SMIN"},
                    {"period": 2, "attribute": "OV_SMIN"},
                    {"period": 3, "attribute": "ZOM_SMIN"},
                ],
                "hmin": "HARDMIN",
            },
        }
    ],
)

mswloc = LocationSet(
    name="mswlocaties",
    fews_name="MSW_STATIONS",
    checker_property_name="mswloc",
    validation_rules=[],
)

psloc = LocationSet(
    name="peilschalen",
    fews_name="OPVLWATER_PEILSCHALEN",
    checker_property_name="",  # TODO
    validation_rules=[],
)
