from collections import namedtuple
from enum import Enum
from mptconfig.fews_utilities import FewsConfig
from mptconfig.fews_utilities import xml_to_dict
from pathlib import Path
from typing import Dict
from typing import List

import geopandas as gpd
import re


# Handy constant for building relative paths
BASE_DIR = Path(__file__).parent.parent
PathNamedTuple = namedtuple("Paths", ["is_file", "should_exist", "path", "description"])


class PathConstants1(Enum):
    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=BASE_DIR / "data" / "output" / "result.xlsx",
        description="",
    )
    histtags_csv = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20200930.csv",
        description="",
    )
    fews_config = PathNamedTuple(
        is_file=False,
        should_exist=True,
        path=Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config",
        description="",
    )
    output_dir = PathNamedTuple(is_file=False, should_exist=True, path=BASE_DIR / "data" / "output", description="")
    ignored_exloc = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_exloc.csv",
        description="externalLocations die worden overgeslagen bij rapportage exLoc error",
    )
    ignored_histtag = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_histtag.csv",
        description="histTags die worden genegeerd bij het wegschrijven van de sheet mpt",
    )
    ignored_ts800 = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_ts800.csv",
        description="Locations die worden overgeslagen bij rapportage timeSeries error",
    )
    ignored_xy = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_xy.csv",
        description="CAW-locaties waarbij controle op consistente xy locatie in locSet error wordt overgeslagen",
    )


EXPECTED_SUMMARY1 = {
    "idmap section error": 36,
    "ignored histTags match": 0,
    "histTags noMatch": 56,
    "idmaps double": 0,
    "mpt_histtags_new": 1770,
    "pars missing": 1,
    "hloc error": 0,
    "exPar error": 91,  # dit was 2 met daniel's len(ex_par_error) > 0 | any(errors.values()). Met 'or' ipv '|' dus 91
    "intLoc missing": 2,
    "exPar missing": 338,
    "exLoc error": 8,
    "timeSeries error": 62,
    "validation error": 273,
    "par mismatch": 0,
    "locSet error": 319,
}


class PathConstants2(Enum):
    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=BASE_DIR / "data" / "output" / "result.xlsx",
        description="",
    )
    histtags_csv = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
        description="",
    )
    fews_config = PathNamedTuple(
        is_file=False,
        should_exist=True,
        path=Path("D:") / "WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config",
        description="",
    )
    output_dir = PathNamedTuple(is_file=False, should_exist=True, path=BASE_DIR / "data" / "output", description="")
    ignored_exloc = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_exloc.csv",
        description="externalLocations die worden overgeslagen bij rapportage exLoc error",
    )
    ignored_histtag = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_histtag.csv",
        description="histTags die worden genegeerd bij het wegschrijven van de sheet mpt",
    )
    ignored_ts800 = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_ts800.csv",
        description="Locations die worden overgeslagen bij rapportage timeSeries error",
    )
    ignored_xy = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_xy.csv",
        description="CAW-locaties waarbij controle op consistente xy locatie in locSet error wordt overgeslagen",
    )


EXPECTED_SUMMARY2 = {
    "idmap section error": 34,
    "ignored histTags match": 1,
    "histTags noMatch": 15,
    "idmaps double": 0,
    "mpt_histtags_new": 1802,
    "pars missing": 0,
    "hloc error": 18,
    "exPar error": 89,  # dit was 2 met daniel's len(ex_par_error) > 0 | any(errors.values()). Met 'or' ipv '|' dus 91
    "intLoc missing": 0,
    "exPar missing": 346,
    "exLoc error": 5,
    "timeSeries error": 7,
    "validation error": 708,
    "par mismatch": 0,
    "locSet error": 335,
}


class PathConstants3(Enum):
    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=BASE_DIR / "data" / "output" / "result.xlsx",
        description="",
    )
    histtags_csv = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
        description="",
    )
    fews_config = PathNamedTuple(
        is_file=False,
        should_exist=True,
        path=Path("D:") / "WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT" / "FEWS_SA" / "config",
        description="",
    )
    output_dir = PathNamedTuple(is_file=False, should_exist=True, path=BASE_DIR / "data" / "output", description="")
    ignored_exloc = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_exloc.csv",
        description="externalLocations die worden overgeslagen bij rapportage exLoc error",
    )
    ignored_histtag = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_histtag.csv",
        description="histTags die worden genegeerd bij het wegschrijven van de sheet mpt",
    )
    ignored_ts800 = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_ts800.csv",
        description="Locations die worden overgeslagen bij rapportage timeSeries error",
    )
    ignored_xy = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_xy.csv",
        description="CAW-locaties waarbij controle op consistente xy locatie in locSet error wordt overgeslagen",
    )


EXPECTED_SUMMARY3 = {
    "idmap section error": 36,
    "ignored histTags match": 0,
    "histTags noMatch": 69,
    "idmaps double": 0,
    "mpt_histtags_new": 1770,
    "pars missing": 1,
    "hloc error": 0,
    "exPar error": 91,  # dit was 2 met daniel's len(ex_par_error) > 0 | any(errors.values()). Met 'or' ipv '|' dus 91
    "intLoc missing": 2,
    "exPar missing": 338,
    "exLoc error": 8,
    "timeSeries error": 62,
    "validation error": 273,
    "par mismatch": 0,
    "locSet error": 319,
}


class PathConstants4(Enum):
    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=BASE_DIR / "data" / "output" / "result.xlsx",
        description="",
    )
    histtags_csv = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
        description="",
    )
    fews_config = PathNamedTuple(
        is_file=False,
        should_exist=True,
        path=Path("D:") / "WIS_6.0_ONTWIKKEL_202002_RK" / "FEWS_SA" / "config",
        description="",
    )
    output_dir = PathNamedTuple(is_file=False, should_exist=True, path=BASE_DIR / "data" / "output", description="")
    ignored_exloc = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_exloc.csv",
        description="externalLocations die worden overgeslagen bij rapportage exLoc error",
    )
    ignored_histtag = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_histtag.csv",
        description="histTags die worden genegeerd bij het wegschrijven van de sheet mpt",
    )
    ignored_ts800 = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_ts800.csv",
        description="Locations die worden overgeslagen bij rapportage timeSeries error",
    )
    ignored_xy = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_xy.csv",
        description="CAW-locaties waarbij controle op consistente xy locatie in locSet error wordt overgeslagen",
    )


EXPECTED_SUMMARY4 = {
    "idmap section error": 34,
    "ignored histTags match": 1,
    "histTags noMatch": 15,
    "idmaps double": 0,
    "mpt_histtags_new": 1802,
    "pars missing": 0,
    "hloc error": 18,
    "exPar error": 89,  # dit was 2 met daniel's len(ex_par_error) > 0 | any(errors.values()). Met 'or' ipv '|' dus 91
    "intLoc missing": 0,
    "exPar missing": 346,
    "exLoc error": 5,
    "timeSeries error": 7,
    "validation error": 955,
    "par mismatch": 0,
    "locSet error": 335,
}

PathConstants = PathConstants4
EXPECTED_SUMMARY = EXPECTED_SUMMARY4


class LocationSet:
    def __init__(
        self,
        name: str,
        fews_name: str,
        checker_property_name: str,
        idmap_section_name: str,
        validation_rules: List[Dict],
    ):
        self.name = name
        self.fews_name = fews_name
        self.checker_property_name = checker_property_name
        self.idmap_section_name = idmap_section_name
        self.validation_rules = validation_rules
        self.fews_config = FewsConfig(path=PathConstants.fews_config.value.path)
        self._data = None
        self._csvfile_meta = None
        self._attrib_files = None
        self._fews_location_set = None

    @property
    def geo_df(self) -> gpd.GeoDataFrame:
        if self._data is not None:
            return self._data
        self._data = self.fews_config.get_locations(location_set_key=self.fews_name)
        return self._data

    @property
    def csvfile_meta(self) -> Dict[str, str]:
        """
        e.g. {
                'file': 'oppvlwater_hoofdloc',
                'geoDatum': 'Rijks Driehoekstelsel',
                'id': '%LOC_ID%',
                'name': '%LOC_NAME%',
                'description': 'Hoofdlocaties oppervlaktewater',
                etc..
            }
        """
        if self._csvfile_meta is not None:
            return self._csvfile_meta
        locations_dict = xml_to_dict(xml_filepath=self.fews_config.RegionConfigFiles["LocationSets"])
        location_sets = locations_dict["locationSets"]["locationSet"]
        csvfile_meta = [locset for locset in location_sets if locset["id"] == self.fews_name]
        assert len(csvfile_meta) == 1
        self._csvfile_meta = csvfile_meta[0]["csvFile"]
        return self._csvfile_meta

    @property
    def csvfile(self) -> str:
        """ e.g. 'oppvlwater_hoofdloc' """
        return self.csvfile_meta["file"]

    @property
    def attrib_files(self):
        if self._attrib_files is not None:
            return self._attrib_files
        attribute_files = self.csvfile_meta["attributeFile"]
        if not isinstance(attribute_files, list):
            attribute_files = [attribute_files]
        self._attrib_files = [attrib_file for attrib_file in attribute_files if "attribute" in attrib_file.keys()]
        return self._attrib_files

    def get_validation_attributes(self, int_pars: List[str] = None) -> List[str]:
        """Get attributes (as a list) from validation rules (nested dict).

        Example:
            validation_rules = [
                {
                    'parameter': 'H.R.',
                    'extreme_values': {'hmax': 'HR1_HMAX', 'hmin': 'HR1_HMIN'}
                },
                {
                    'parameter': 'H2.R.',
                    'extreme_values': {'hmax': 'HR2_HMAX', 'hmin': 'HR2_HMIN'}
                },
                    etc..
                ]

            get_validation_attributes(int_pars=None) returns: ['HR1_HMAX', 'HR1_HMIN', 'HR2_HMAX', 'HR2_HMIN',]
        """
        if int_pars is None:
            int_pars = [rule["parameter"] for rule in self.validation_rules]
        result = []
        for rule in self.validation_rules:
            if not any(re.match(pattern=rule["parameter"], string=int_par) for int_par in int_pars):
                continue
            for attribute in rule["extreme_values"].values():
                if isinstance(attribute, list):
                    result += [value["attribute"] for value in attribute]
                else:
                    result += [attribute]
        return result


hoofdlocationset = LocationSet(
    name="hoofdlocaties",
    fews_name="OPVLWATER_HOOFDLOC",
    checker_property_name="hoofdloc",
    idmap_section_name="KUNSTWERKEN",
    validation_rules=[
        {"parameter": "H.S.", "extreme_values": {"hmax": "HS1_HMAX", "hmin": "HS1_HMIN"}},
        {"parameter": "H2.S.", "extreme_values": {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}},
        {"parameter": "H3.S.", "extreme_values": {"hmax": "HS3_HMAX", "hmin": "HS3_HMIN"}},
    ],
)

sublocationset = LocationSet(
    name="sublocaties",
    fews_name="OPVLWATER_SUBLOC",
    checker_property_name="subloc",
    idmap_section_name="KUNSTWERKEN",
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


waterstandlocationset = LocationSet(
    name="waterstandlocaties",
    fews_name="OPVLWATER_WATERSTANDEN_AUTO",
    checker_property_name="waterstandloc",
    idmap_section_name="WATERSTANDLOCATIES",
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


mswlocationset = LocationSet(
    name="mswlocaties",
    fews_name="MSW_STATIONS",
    checker_property_name="mswloc",
    idmap_section_name="",
    validation_rules=[],
)

pslocationset = LocationSet(
    name="peilschalen",
    fews_name="OPVLWATER_PEILSCHALEN",
    checker_property_name="",  # TODO
    idmap_section_name="",
    validation_rules=[],
)


class LocationSetChoices(Enum):
    hoofdloc = hoofdlocationset
    subloc = sublocationset
    waterstandloc = waterstandlocationset
    mswloc = mswlocationset
    psloc = pslocationset

    @property
    def skip_check_location_set_error(self) -> bool:
        return self not in {self.hoofdloc, self.subloc, self.waterstandloc}


IDMAP_FILES = [
    "IdOPVLWATER",
    "IdOPVLWATER_HYMOS",
    "IdHDSR_NSC",
    "IdOPVLWATER_WQ",
    "IdGrondwaterCAW",
]

IDMAP_SECTIONS = {
    "IdOPVLWATER_HYMOS": {
        "KUNSTWERKEN": [{"section_end": "<!--WATERSTANDSLOCATIES-->"}],
        "WATERSTANDLOCATIES": [{"section_start": "<!--WATERSTANDSLOCATIES-->", "section_end": "<!--OVERIG-->"}],
    },
    "IdOPVLWATER": {
        "KUNSTWERKEN": [
            {
                "section_start": "<!--KUNSTWERK SUBLOCS (old CAW id)-->",
                "section_end": "<!--WATERSTANDSLOCATIES (old CAW id)-->",
            },
            {
                "section_start": "<!--KUNSTWERK SUBLOCS (new CAW id)-->",
                "section_end": "<!--WATERSTANDSLOCATIES (new CAW id)-->",
            },
        ],
        "WATERSTANDLOCATIES": [
            {"section_start": "<!--WATERSTANDSLOCATIES (old CAW id)-->", "section_end": "<!--MSW (old CAW id)-->"},
            {"section_start": "<!--WATERSTANDSLOCATIES (new CAW id)-->", "section_end": "<!--MSW (new CAW id)-->"},
        ],
        "MSWLOCATIES": [{"section_start": "<!--MSW (new CAW id)-->"}],
    },
}

SECTION_TYPE_PREFIX_MAPPER = {
    "KUNSTWERKEN": "KW",
    "WATERSTANDLOCATIES": "OW",
    "MSWLOCATIES": "(OW|KW)",
}

EXTERNAL_PARAMETERS_ALLOWED = {
    "pompvijzel": ["FQ.$", "I.B$", "IB.$", "I.H$", "IH.$", "I.L$", "IL.$", "Q.$", "TT.$"],
    "stuw": ["SW.$", "Q.$", "ES.$"],
    "schuif": ["ES.$", "SP.$", "SS.$", "Q.$", "SM.$"],
    "afsluiter": ["ES.$"],
    "debietmeter": ["Q.$"],
    "vispassage": ["ES.$", "SP.$", "SS.$", "Q.$"],
    "krooshek": ["HB.$", "HO.$"],
    "waterstand": ["HB.$", "HO.$", "H$"],  # TODO: @Roger: moet deze laatste niet H.$ zijn ?!?
}

PARAMETER_MAPPING = [
    {"internal": "DD.", "external": "I.B"},
    {"internal": "DDH.", "external": "I.H"},
    {"internal": "DDL.", "external": "I.L"},
    {"internal": "ES.", "external": "ES."},
    {"internal": "ES2.", "external": "ES."},
    {"internal": "F.", "external": "FQ."},
    {"internal": "H.G.", "external": "H"},
    {"internal": "H.G.", "external": "HB."},
    {"internal": "H.G.", "external": "HO."},
    {"internal": "H.S.", "external": "HS."},
    {"internal": "H.R.", "external": "HR."},
    {"internal": "H2.R.", "external": "HR."},
    {"internal": "H2.S.", "external": "HS."},
    {"internal": "H3.R.", "external": "HR."},
    {"internal": "H3.S.", "external": "HS."},
    {"internal": "Hastr.", "external": "HA"},
    {"internal": "Hh.", "external": "SM."},
    {"internal": "Hh.", "external": "SS."},
    {"internal": "Hk.", "external": "SW."},
    {"internal": "IB.", "external": "IB."},
    {"internal": "IBH.", "external": "IH."},
    {"internal": "IBL.", "external": "IL."},
    {"internal": "POS.", "external": "SP."},
    {"internal": "POS2.", "external": "SP."},
    {"internal": "Q.G.", "external": "Q."},
    {"internal": "Q.R.", "external": "QR1"},
    {"internal": "Q.S.", "external": "QS1"},
    {"internal": "Q2.R.", "external": "QR2"},
    {"internal": "Q2.S.", "external": "QS2"},
    {"internal": "Q3.R.", "external": "QR3"},
    {"internal": "Q3.S.", "external": "QS3"},
    {"internal": "Qipcl.G.", "external": "Q."},
    {"internal": "TT.", "external": "TT."},
    {"internal": "WR.", "external": "WR"},
    {"internal": "WS.", "external": "WS"},
]

def check_constants():
    # check 1: BASE_DIR's name
    assert (
        BASE_DIR.name == "mptconfig_checker"
    ), f"BASE_DIR name ={BASE_DIR.name} should be project's root 'mptconfig_checker'"

    # check 2: PathConstants has exactly the following objects
    all_defined_paths = [constant.name for constant in PathConstants]
    expected_paths = [
        "result_xlsx",
        "fews_config",
        "histtags_csv",
        "ignored_exloc",
        "ignored_histtag",
        "ignored_ts800",
        "ignored_xy",
        "output_dir",
    ]
    assert len(all_defined_paths) == len(expected_paths) == len(set(expected_paths))
    too_many = set(all_defined_paths).difference(expected_paths)
    too_few = set(expected_paths).difference(all_defined_paths)
    assert not too_many, f"too many paths {too_many}"
    assert not too_few, f"too few paths {too_few}"

    # check 3: check if files and dirs exist if the are expected to. And visa versa
    for path_namedtuple in PathConstants:
        if not isinstance(path_namedtuple.value.path, Path):
            raise AssertionError(f"{path_namedtuple.name}'s path is not of type pathlib.Path")
        if not path_namedtuple.value.should_exist:
            # TODO: activate this check
            # assert not path_namedtuple.path.exists(), f"path {path_namedtuple.path} should not exist"
            continue
        if path_namedtuple.value.is_file:
            assert path_namedtuple.value.path.is_file(), f"file should exist {path_namedtuple.value.path}"
        else:
            assert path_namedtuple.value.path.is_dir(), f"dir should exists {path_namedtuple.value.path}"


check_constants()
