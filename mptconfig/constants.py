from collections import namedtuple
from datetime import datetime
from enum import Enum
from mptconfig.fews_utilities import FewsConfig
from mptconfig.fews_utilities import xml_to_dict
from pathlib import Path
from typing import Dict
from typing import List

import geopandas as gpd
import logging
import pandas as pd  # noqa pandas comes with geopandas
import re


logger = logging.getLogger(__name__)

# Handy constant for building relative paths
BASE_DIR = Path(__file__).parent.parent
assert BASE_DIR.name == "mptconfig_checker"

# do not change these paths
D_DRIVE = Path("D:")
S_DRIVE = Path("S:")
S_WATERBALANS_WIS_CAW_DIR = S_DRIVE / "Waterbalans" / "_WIS_" / "caw"


PathNamedTuple = namedtuple("Paths", ["is_file", "should_exist", "path", "description"])
YYYYMMDD_TODAY = datetime.now().strftime("%Y%m%d_%H%M%S")

# TODO: ask roger: veel locaties hebben start=19000101 en end=21000101 (bijv in validatie csv): dus
#  start=STARTDATE_UNMEASURED_LOC, end=MAX_ENDDATE_MEASURED_LOC. Echter, dan klopt die naam van die
#  dummy dates niet. Wat zijn betere namen?
# sublocs without timeseries are unmeasered (in dutch 'onbemeten locaties') and have dummy dates
STARTDATE_UNMEASURED_LOC = pd.Timestamp(year=1900, month=1, day=1)
ENDDATE_UNMEASURED_LOC = pd.Timestamp(
    year=2222, month=11, day=11
)  # 32101230 is not possible anymore as pd.Timestamp.max = '2262-04-11'
MAX_ENDDATE_MEASURED_LOC = pd.Timestamp(year=2100, month=1, day=1)
MIN_DATE_ALLOWED = pd.Timestamp(year=1989, month=10, day=28)
MAX_DATE_ALLOWED = pd.Timestamp.now()

# TODO: come up with better name then 'MAX_DIFF' and move to constants
MAX_DIFF = pd.Timedelta(weeks=26)
# 26 weken = 6 maanden
# Bestaat dat meetpunt nog? Is het nog operationeel?
# -	kijken naar alle gekoppelde tijdreeksen (startenddate) van dat punt
# -	Roger geeft niet zomaar eindpunt aan een meetpunt (wellicht werkzaamheden aan meetpunt, nog steeds in renovatie?).
#   Door schade en schande hanteert Roger nu 6 maanden geen tijdreeks?
#   Na 6 maanden geen tijdreeks data meer ontvangen? Dan eindpunt toekennen.


# als in idmapping tijdreeks voorkomt die niet in get_series_enddate voor komt
# dat wat in S:\Waterbalans\_WIS_\caw\get_series_startenddate\CAW_mpt_startenddate\ too_much.csv staat
# moet de checker ook ergens teruggeven


class PathConstants(Enum):
    """Paths to be changes if you run the checker. """

    result_xlsx = PathNamedTuple(
        is_file=True,
        should_exist=False,
        path=BASE_DIR / "data" / "output" / f"result_{YYYYMMDD_TODAY}.xlsx",
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
        path=D_DRIVE / "WIS_6.0_MPTCONFIG_201902" / "FEWS_SA" / "config",
        description="",
    )
    output_dir = PathNamedTuple(is_file=False, should_exist=True, path=BASE_DIR / "data" / "output", description="")
    ignored_ex_loc = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_ex_loc.csv",
        description="externalLocations die worden overgeslagen bij rapportage ex loc error",
    )
    ignored_histtag = PathNamedTuple(
        is_file=True,
        should_exist=True,
        # path=BASE_DIR / "data" / "input" / "ignored_histtag.csv",
        path=S_WATERBALANS_WIS_CAW_DIR
        / "get_series_startenddate"
        / "CAW_mpt_startenddate"
        / "mpt_startenddate_total_pixml_transferdb_ignore.csv",
        description="histTags die worden genegeerd bij het wegschrijven van de sheet mpt",
    )
    ignored_time_series_error = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_time_series_error.csv",
        description="internalLocation die worden overgeslagen bij rapportage time_series_error",
    )
    ignored_ts800 = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_ts800.csv",
        description="Locations die worden overgeslagen bij rapportage time_series error",
    )
    ignored_xy = PathNamedTuple(
        is_file=True,
        should_exist=True,
        path=BASE_DIR / "data" / "input" / "ignored_xy.csv",
        description="CAW-locaties waarbij controle op consistente xy locatie in loc_set error wordt overgeslagen",
    )


class SubLocTypeChoices(Enum):
    pompvijzel = "pompvijzel"
    krooshek = "krooshek"
    stuw = "stuw"
    totaal = "totaal"
    vispassage = "vispassage"
    schuif = "schuif"
    debietmeter = "debietmeter"
    overlaat = "overlaat"
    afsluiter = "afsluiter"


class LocationSet:
    def __init__(self, fews_config: FewsConfig = None, fews_config_path: Path = None):
        assert (fews_config and not fews_config_path) or (
            fews_config_path and not fews_config
        ), "use either path or config"
        self.fews_config_path = fews_config_path
        self._fews_config = fews_config
        self._geo_df = None
        self._general_location_sets_dict = None
        self._csvfile_meta = None
        self._attrib_files = None

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def fews_name(self) -> str:
        raise NotImplementedError

    @property
    def idmap_section_name(self) -> str:
        raise NotImplementedError

    @property
    def skip_check_location_set_error(self) -> bool:
        raise NotImplementedError

    @property
    def validation_rules(self) -> Dict:
        raise NotImplementedError

    @property
    def fews_config(self) -> FewsConfig:
        if self._fews_config is not None:
            return self._fews_config
        self._fews_config = FewsConfig(path=self.fews_config_path)
        return self._fews_config

    @property
    def geo_df(self) -> gpd.GeoDataFrame:
        if self._geo_df is not None:
            return self._geo_df
        self._geo_df = self.fews_config.get_locations(location_set_key=self.fews_name)
        assert isinstance(self._geo_df, gpd.GeoDataFrame)
        return self._geo_df

    @property
    def general_location_sets_dict(self) -> Dict:
        if self._general_location_sets_dict is not None:
            return self._general_location_sets_dict
        location_sets_file_path = self.fews_config.RegionConfigFiles["LocationSets"]
        location_sets_dict = xml_to_dict(xml_filepath=location_sets_file_path)
        self._general_location_sets_dict = location_sets_dict["locationSets"]["locationSet"]
        # ensure unique ids, e.g. 'OPVLWATER_HOOFDLOC', 'OPVLWATER_SUBLOC', 'RWZI', ..
        ids = [x["id"] for x in self._general_location_sets_dict]
        assert len(set(ids)) == len(ids), "we expected unique id's in RegionConfigFiles LocationSets"
        return self._general_location_sets_dict

    @property
    def csv_file_meta(self) -> Dict:
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
        csvfile_meta = [loc_set for loc_set in self.general_location_sets_dict if loc_set["id"] == self.fews_name]
        assert len(csvfile_meta) == 1
        self._csvfile_meta = csvfile_meta[0]["csvFile"]
        return self._csvfile_meta

    @property
    def csv_filename(self) -> str:
        """ e.g. 'oppvlwater_hoofdloc' """
        return self.csv_file_meta["file"]

    @property
    def attrib_files(self) -> List:
        if self._attrib_files is not None:
            return self._attrib_files
        attribute_files = self.csv_file_meta.get("attributeFile", None)
        if not attribute_files:
            self._attrib_files = []
            return self._attrib_files
        if not isinstance(attribute_files, list):
            attribute_files = [attribute_files]
        assert all(
            [isinstance(attrib_file, dict) for attrib_file in attribute_files]
        ), "attribute_files must be list with dicts"
        self._attrib_files = [attrib_file for attrib_file in attribute_files if "attribute" in attrib_file]
        return self._attrib_files

    def get_validation_attributes(self, int_pars: List[str] = None) -> List[str]:
        """Get attributes (as a list) from validation rules (list with nested dicts).

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

            get_validation_attributes(int_pars=None) returns: ['HR1_HMAX', 'HR1_HMIN', 'HR2_HMAX', 'HR2_HMIN']
        """
        if not int_pars:
            logger.debug(f"returning all validation parameters for locationset {self.name}")
            int_pars = [rule["parameter"] for rule in self.validation_rules]
        result = []
        for rule in self.validation_rules:
            if not any(re.match(pattern=rule["parameter"], string=int_par) for int_par in int_pars):
                continue
            result.extend(rule["extreme_values"].values())
        return result


class HoofdLocationSet(LocationSet):
    @property
    def name(self):
        return "hoofdlocaties"

    @property
    def fews_name(self):
        return "OPVLWATER_HOOFDLOC"

    @property
    def idmap_section_name(self):
        return "KUNSTWERKEN"

    @property
    def skip_check_location_set_error(self):
        return False

    @property
    def validation_rules(self):
        return [
            {"parameter": "H.S.", "extreme_values": {"hmax": "HS1_HMAX", "hmin": "HS1_HMIN"}},
            {"parameter": "H2.S.", "extreme_values": {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}},
            {"parameter": "H3.S.", "extreme_values": {"hmax": "HS3_HMAX", "hmin": "HS3_HMIN"}},
        ]


class SubLocationSet(LocationSet):
    @property
    def name(self):
        return "sublocaties"

    @property
    def fews_name(self):
        return "OPVLWATER_SUBLOC"

    @property
    def idmap_section_name(self):
        return "KUNSTWERKEN"

    @property
    def skip_check_location_set_error(self):
        return False

    @property
    def validation_rules(self):
        return [
            {"parameter": "H.R.", "extreme_values": {"hmax": "HR1_HMAX", "hmin": "HR1_HMIN"}},
            {"parameter": "H2.R.", "extreme_values": {"hmax": "HR2_HMAX", "hmin": "HR2_HMIN"}},
            {"parameter": "H3.R.", "extreme_values": {"hmax": "HR3_HMAX", "hmin": "HR3_HMIN"}},
            {"parameter": "F.", "extreme_values": {"hmax": "FRQ_HMAX", "hmin": "FRQ_HMIN"}},
            {"parameter": "Hh.", "extreme_values": {"hmax": "HEF_HMAX", "hmin": "HEF_HMIN"}},
            {
                "parameter": "POS.",
                "extreme_values": {"hmax": "PERC_HMAX", "smax": "PERC_SMAX", "smin": "PERC_SMIN", "hmin": "PERC_HMIN"},
            },
            {
                "parameter": "POS2.",
                "extreme_values": {
                    "hmax": "PERC2_HMAX",
                    "smax": "PERC2_SMAX",
                    "smin": "PERC2_SMIN",
                    "hmin": "PERC2_HMIN",
                },
            },
            {"parameter": "TT.", "extreme_values": {"hmax": "TT_HMAX", "hmin": "TT_HMIN"}},
            # HDSR does not yet have validation CSVs for berekend debiet
            # {"parameter": "Q.B.",
            #  "extreme_values": {"hmax": "Q_HMAX", "smax": "Q_SMAX", "smin": "Q_SMIN", "hmin": "Q_HMIN"}},
            {
                "parameter": "Q.G.",
                "extreme_values": {"hmax": "Q_HMAX", "smax": "Q_SMAX", "smin": "Q_SMIN", "hmin": "Q_HMIN"},
            },
            # TODO: add krooshek
        ]


class WaterstandLocationSet(LocationSet):
    @property
    def name(self):
        return "waterstandlocaties"

    @property
    def fews_name(self):
        return "OPVLWATER_WATERSTANDEN_AUTO"

    @property
    def idmap_section_name(self):
        return "WATERSTANDLOCATIES"

    @property
    def skip_check_location_set_error(self):
        return False

    @property
    def validation_rules(self):
        return [
            {
                "parameter": "H.G.",
                "extreme_values": {
                    "hmax": "HARDMAX",
                    "smax_win": "WIN_SMAX",
                    "smax_ov": "OV_SMAX",
                    "smax_zom": "ZOM_SMAX",
                    "smin_win": "WIN_SMIN",
                    "smin_ov": "OV_SMIN",
                    "smin_zom": "ZOM_SMIN",
                    "hmin": "HARDMIN",
                },
            }
        ]


class MswLocationSet(LocationSet):
    @property
    def name(self):
        return "mswlocaties"

    @property
    def fews_name(self):
        return "MSW_STATIONS"

    @property
    def idmap_section_name(self):
        return ""

    @property
    def skip_check_location_set_error(self):
        return True

    @property
    def validation_rules(self):
        return []


class PeilschaalLocationSet(LocationSet):
    @property
    def name(self):
        return "peilschalen"

    @property
    def fews_name(self):
        return "OPVLWATER_PEILSCHALEN"

    @property
    def idmap_section_name(self):
        return ""

    @property
    def skip_check_location_set_error(self):
        return True

    @property
    def validation_rules(self):
        return []


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
    "stuw": ["SW.$", "Q.$"],
    "schuif": ["ES.$", "SP.$", "SS.$", "Q.$", "SM.$"],
    "afsluiter": ["ES.$"],
    "debietmeter": ["Q.$"],
    "vispassage": ["ES.$", "SP.$", "SS.$", "Q.$"],
    "krooshek": ["HB.$", "HO.$"],
    "waterstand": ["HB.$", "HO.$", "H.$"],
}


class ValidationCsvChoices(Enum):
    oppvlwater_kunstvalidatie_debiet = "oppvlwater_kunstvalidatie_debiet"
    oppvlwater_watervalidatie = "oppvlwater_watervalidatie"
    oppvlwater_kunstvalidatie_kroos = "oppvlwater_kunstvalidatie_kroos"
    oppvlwater_kunstvalidatie_freq = "oppvlwater_kunstvalidatie_freq"
    oppvlwater_kunstvalidatie_hefh = "oppvlwater_kunstvalidatie_hefh"
    oppvlwater_kunstvalidatie_kruinh = "oppvlwater_kunstvalidatie_kruinh"
    oppvlwater_kunstvalidatie_schuifp = "oppvlwater_kunstvalidatie_schuifp"
    oppvlwater_kunstvalidatie_schuifp2 = "oppvlwater_kunstvalidatie_schuifp2"
    oppvlwater_kunstvalidatie_streef1 = "oppvlwater_kunstvalidatie_streef1"
    oppvlwater_kunstvalidatie_streef2 = "oppvlwater_kunstvalidatie_streef2"
    oppvlwater_kunstvalidatie_streef3 = "oppvlwater_kunstvalidatie_streef3"
    oppvlwater_kunstvalidatie_stuur1 = "oppvlwater_kunstvalidatie_stuur1"
    oppvlwater_kunstvalidatie_stuur2 = "oppvlwater_kunstvalidatie_stuur2"
    oppvlwater_kunstvalidatie_stuur3 = "oppvlwater_kunstvalidatie_stuur3"
    oppvlwater_kunstvalidatie_toert = "oppvlwater_kunstvalidatie_toert"

    @classmethod
    def get_validation_csv_name(cls, int_par: str, loc_type: str) -> str:
        match = [
            int_par_regex
            for int_par_regex in INTPAR_2_VALIDATION_CSV.keys()
            if re.match(pattern=int_par_regex, string=int_par)
        ]
        if not match:
            logger.debug(f"no validation csv found: int_par={int_par} not in INTPAR_2_VALIDATION_CSV.keys")
            return ""
        assert len(match) == 1
        mapper = INTPAR_2_VALIDATION_CSV[match[0]]
        filename = mapper.get(loc_type, None)
        if not filename:
            logger.debug(
                f"no validation csv found: int_par={int_par} has only loc_types={mapper.keys()}, no {loc_type}"
            )
        return filename


INTPAR_2_VALIDATION_CSV = {
    "H.G.": {
        "waterstand": ValidationCsvChoices.oppvlwater_watervalidatie.value,
        "krooshek": ValidationCsvChoices.oppvlwater_kunstvalidatie_kroos.value,
    },
    "Hh.": {
        "schuif": ValidationCsvChoices.oppvlwater_kunstvalidatie_hefh.value,
        "vispassage": ValidationCsvChoices.oppvlwater_kunstvalidatie_hefh.value,
    },
    "Q.G.": {
        # we only validate it for debietmeters (not schuif, vispassage, pompvijzel, stuw)
        "debietmeter": ValidationCsvChoices.oppvlwater_kunstvalidatie_debiet.value
    },
    "F.": {"pompvijzel": ValidationCsvChoices.oppvlwater_kunstvalidatie_freq.value},
    "Hk.": {"stuw": ValidationCsvChoices.oppvlwater_kunstvalidatie_kruinh.value},
    "POS.": {"schuif": ValidationCsvChoices.oppvlwater_kunstvalidatie_schuifp.value},
    "POS2.": {"schuif": ValidationCsvChoices.oppvlwater_kunstvalidatie_schuifp2.value},
    "H.S.": {"waterstand": ValidationCsvChoices.oppvlwater_kunstvalidatie_streef1.value},
    "H2.S.": {"waterstand": ValidationCsvChoices.oppvlwater_kunstvalidatie_streef2.value},
    "H3.S.": {"waterstand": ValidationCsvChoices.oppvlwater_kunstvalidatie_streef3.value},
    "H.R.": {"waterstand": ValidationCsvChoices.oppvlwater_kunstvalidatie_stuur1.value},
    "H2.R.": {"waterstand": ValidationCsvChoices.oppvlwater_kunstvalidatie_stuur2.value},
    "H3.R.": {"waterstand": ValidationCsvChoices.oppvlwater_kunstvalidatie_stuur3.value},
    "TT.": {"pompvijzel": ValidationCsvChoices.oppvlwater_kunstvalidatie_toert.value},
}


"""
{"internal": "DD.", "external": "I.B"}, --> wordt niet gevalideerd
{"internal": "DDH.", "external": "I.H"}, --> wordt niet gevalideerd
{"internal": "DDL.", "external": "I.L"}, --> wordt niet gevalideerd
{"internal": "ES.", "external": "ES."}, --> wordt niet gevalideerd, want 0/1
{"internal": "ES2.", "external": "ES."}, --> wordt niet gevalideerd, want 0/1
# {"internal": "F.", "external": "FQ."},
{"internal": "H.G.", "external": "HG"}, --> moet bij krooshek
{"internal": "H.G.", "external": "HB."},  --> moet bij krooshek
{"internal": "H.G.", "external": "HO."}, --> moet bij krooshek
# {"internal": "H.S.", "external": "HS."},
# {"internal": "H.R.", "external": "HR."},
# {"internal": "H2.R.", "external": "HR."},
# {"internal": "H2.S.", "external": "HS."},
# {"internal": "H3.R.", "external": "HR."},
# {"internal": "H3.S.", "external": "HS."},
{"internal": "Hastr.", "external": "HA"}, # noqa astronomisch peil (komt bij MSW 1x voor), msw reeks wordt niet gevalideerd, want externe reeks
# {"internal": "Hh.", "external": "SM."},
# {"internal": "Hh.", "external": "SS."},
# {"internal": "Hk.", "external": "SW."},
{"internal": "IB.", "external": "IB."}, --> wordt niet gevalideerd, want 0/1
{"internal": "IBH.", "external": "IH."}, --> wordt niet gevalideerd, want 0/1
{"internal": "IBL.", "external": "IL."}, --> wordt niet gevalideerd, want 0/1
# {"internal": "POS.", "external": "SP."},
# {"internal": "POS2.", "external": "SP."},
{"internal": "Q.G.", "external": "Q."}, # noqa debiet CAW beschouwen we in wis als .. (in kunstvalidatie_debiet.csv staan alleen debietmeters!)
{"internal": "Q.R.", "external": "QR1"},
{"internal": "Q.S.", "external": "QS1"},
{"internal": "Q2.R.", "external": "QR2"},
{"internal": "Q2.S.", "external": "QS2"},
{"internal": "Q3.R.", "external": "QR3"},
{"internal": "Q3.S.", "external": "QS3"},
{"internal": "Qipcl.G.", "external": "Q."},
# {"internal": "TT.", "external": "TT."},
{"internal": "WR.", "external": "WR"}, --> windrichting wordt niet gevalideerd
{"internal": "WS.", "external": "WS"}, --> windsnelheid wordt niet gevalideerd
"""


PARAMETER_MAPPING = [
    {"internal": "DD.", "external": "I.B"},  # DD = draaiduur
    {"internal": "DDH.", "external": "I.H"},  # DDH = draaiduur hoogtoeren
    {"internal": "DDL.", "external": "I.L"},  # DDL = draaiduur laagtoeren
    {"internal": "ES.", "external": "ES."},  # ES = eindstand neer (0/1)
    {"internal": "ES2.", "external": "ES."},
    {"internal": "F.", "external": "FQ."},  # Frequentie regelaar
    {"internal": "H.G.", "external": "HG"},  # HG= gemeten peil
    {"internal": "H.G.", "external": "HB."},  # HB = bovenpeil
    {"internal": "H.G.", "external": "HO."},  # HO = benedenpeil
    {"internal": "H.S.", "external": "HS."},  # HS = streef peil
    {"internal": "H.R.", "external": "HR."},  # HR = stuur peil (regel peil)
    {"internal": "H2.R.", "external": "HR."},
    {"internal": "H2.S.", "external": "HS."},
    {"internal": "H3.R.", "external": "HR."},
    {"internal": "H3.S.", "external": "HS."},
    {"internal": "Hastr.", "external": "HA"},
    {"internal": "Hh.", "external": "SM."},  # Hh=Hefhoogte, SM = schuifstand (m tov onderkant of bovenkant oid)
    {"internal": "Hh.", "external": "SS."},  # Hh=Hefhoogte, SS = schuifstand (mNAP)
    {"internal": "Hk.", "external": "SW."},  # Hk = hoogte kruin, SW = stuwstand (w van weir: ‘SS’ kan natuurlijk niet)
    {"internal": "IB.", "external": "IB."},  # IB = in bedrijf
    {"internal": "IBH.", "external": "IH."},  # IBH = in bedrijf hoogtoeren
    {"internal": "IBL.", "external": "IL."},  # IBL = in bedrijf laagtoeren
    {"internal": "POS.", "external": "SP."},  # POS = openingspercentage schuif, SP=Schuifstand
    {"internal": "POS2.", "external": "SP."},
    {"internal": "Q.G.", "external": "Q."},  # QG = gemeten debiet
    {"internal": "Q.R.", "external": "QR1"},  # QR = stuur debiet
    {"internal": "Q.S.", "external": "QS1"},  # QS = streef debiet
    {"internal": "Q2.R.", "external": "QR2"},
    {"internal": "Q2.S.", "external": "QS2"},
    {"internal": "Q3.R.", "external": "QR3"},
    {"internal": "Q3.S.", "external": "QS3"},
    {
        "internal": "Qipcl.G.",
        "external": "Q.",
    },  # noqa Qipcl.G = gemeten Intern PLC debiet (vorige CAW systeem, debiet werd toen niet op onderstation berekend op een paar uitzondering na: en dat noemde men intern PLC
    {"internal": "TT.", "external": "TT."},  # TT = toerental
    {"internal": "WR.", "external": "WR"},  # Windrichting
    {"internal": "WS.", "external": "WS"},  # Windsnelheid
]


def check_constants_paths():
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
        "ignored_ex_loc",
        "ignored_time_series_error",
        "ignored_histtag",
        "ignored_ts800",
        "ignored_xy",
        "output_dir",
    ]
    assert len(expected_paths) == len(set(expected_paths)), "this check makes no sense.."
    too_many = set(all_defined_paths).difference(expected_paths)
    too_few = set(expected_paths).difference(all_defined_paths)
    assert not too_many, f"too many paths {too_many}"
    assert not too_few, f"too few paths {too_few}"

    # check 3: check if files and dirs exist if the are expected to. And visa versa
    for path_namedtuple in PathConstants:
        if not isinstance(path_namedtuple.value.path, Path):
            raise AssertionError(f"{path_namedtuple.name}'s path is not of type pathlib.Path")
        if not path_namedtuple.value.should_exist:
            assert not path_namedtuple.value.path.exists(), f"path {path_namedtuple.value.path} should not exist"
            continue
        if path_namedtuple.value.is_file:
            assert path_namedtuple.value.path.is_file(), f"file should exist {path_namedtuple.value.path}"
        else:
            assert path_namedtuple.value.path.is_dir(), f"dir should exists {path_namedtuple.value.path}"


HLOC_SLOC_VALIDATION_LOGIC = [
    # one general rules written out in statements
    # 1) hmin <= smin < smax <= hmax
    # - hmin
    ("hmin", "<=", "smin"),
    ("hmin", "<", "smax"),
    ("hmin", "<", "hmax"),
    # - smin
    ("smin", "<", "smax"),
    ("smin", "<", "hmax"),
    # - smax
    ("smax", "<=", "hmax"),
]
WLOC_VALIDATION_LOGIC = [
    # two general rules combined written out in statements
    # 1) hmin <= smin < smax <= hmax
    # 2) WIN <= OV <= ZOM
    # - hmin
    ("hmin", "<=", "smin_zom"),
    ("hmin", "<=", "smin_ov"),
    ("hmin", "<=", "smin_win"),
    #
    ("hmin", "<", "smax_zom"),
    ("hmin", "<", "smax_ov"),
    ("hmin", "<", "smax_win"),
    #
    ("hmin", "<", "hmax"),
    # - smin_win
    ("smin_win", "<=", "smin_ov"),
    ("smin_win", "<=", "smin_zom"),
    #
    ("smin_win", "<", "smax_win"),
    ("smin_win", "<", "smax_ov"),
    ("smin_win", "<", "smax_zom"),
    #
    ("smin_win", "<", "h_max"),
    #
    # - smin_ov
    ("smin_ov", "<=", "smin_zom"),
    #
    ("smin_ov", "<", "smax_win"),
    ("smin_ov", "<", "smax_ov"),
    ("smin_ov", "<", "smax_zom"),
    #
    ("smin_ov", "<", "h_max"),
    # - smin_zom
    ("smin_zom", "<", "smax_win"),
    ("smin_zom", "<", "smax_ov"),
    ("smin_zom", "<", "smin_zom"),
    #
    ("smin_zom", "<", "h_max"),
    # - smax_win
    ("smax_win", "<=", "smax_ov"),
    ("smax_win", "<=", "smax_zom"),
    #
    ("smax_win", "<=", "h_max"),
    # - smax_ov
    ("smax_ov", "<=", "smax_zom"),
    #
    ("smax_ov", "<=", "h_max"),
    # - smax_zom
    ("smax_zom", "<=", "h_max"),
]
