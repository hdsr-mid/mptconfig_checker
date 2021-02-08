from collections import namedtuple
from pathlib import Path


# Handy constant for building relative paths
BASE_DIR = Path(__file__).parent.parent


PathNamedTuple = namedtuple("Paths", ["path", "is_file", "must_exist"])


class Paths:
    consistency_input_xlsx = PathNamedTuple(
        path=BASE_DIR / "data" / "input" / "consistency_input.xlsx", is_file=True, must_exist=True,
    )
    mpt_ignore_csv = PathNamedTuple(
        path=BASE_DIR / "data" / "input" / "mpt_startenddate_total_pixml_transferdb_ignore.csv",
        is_file=True,
        must_exist=True,
    )
    hist_tags_csv = PathNamedTuple(
        path=BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20200930.csv",
        is_file=True,
        must_exist=True,
    )
    fews_config = PathNamedTuple(
        path=Path("C:/") / "Users" / "e6105" / "Downloads" / "201902" / "config", is_file=False, must_exist=True,
    )
    output_dir = PathNamedTuple(
        path=BASE_DIR / "data" / "output", is_file=False, must_exist=False,  # will be created if not exists
    )


PATHS_nr1 = {
    "files": {
        "consistency_input_xlsx": BASE_DIR / "data" / "input" / "consistency_input.xlsx",
        "mpt_ignore_csv": BASE_DIR / "data" / "input" / "mpt_startenddate_total_pixml_transferdb_ignore.csv",
        "hist_tags_csv": BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20200930.csv",
    },
    "dirs": {
        # "fews_config": Path("D:") / "WIS_6.0_ONTWIKKEL_201902" / "FEWS_SA" / "config",
        "fews_config": Path("C:/") / "Users" / "e6105" / "Downloads" / "201902" / "config",
        "output_dir": BASE_DIR / "data" / "output",
    },
    "expected_summary": {
        "idmap section error": 36,
        "histTags ignore match": 0,
        "histTags noMatch": 56,
        "idmaps double": 0,
        "mpt": 1770,
        "pars missing": 1,
        "hloc error": 0,
        "exPar error": 2,
        "intLoc missing": 2,
        "exPar missing": 338,
        "exLoc error": 8,
        "timeSeries error": 62,
        "validation error": 273,
        "par mismatch": 0,
        "locSet error": 319,
    },
    "paden": {
        "consistency_xlsx": "..\\data\\consistency.xlsx",
        "mpt_ignore_csv": "..\\data\\mpt_startenddate_total_pixml_transferdb_ignore.csv",
        "hist_tags_csv": "..\\data\\get_series_startenddate_CAW_summary_total_sorted_20200930.csv",
        "fews_config": "D:\\WIS_6.0_ONTWIKKEL_201902\\FEWS_SA\\config",
        "csv_out": "..\\data\\csv",
    },
}

PATHS_nr2 = {
    "files": {
        "consistency_input_xlsx": BASE_DIR / "data" / "input" / "consistency_input.xlsx",
        "mpt_ignore_csv": BASE_DIR / "data" / "input" / "mpt_startenddate_total_pixml_transferdb_ignore.csv",
        "hist_tags_csv": BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
    },
    "dirs": {
        # "fews_config": Path("D:") / "WIS_6.0_ONTWIKKEL_202101" / "FEWS_SA" / "config",
        "fews_config": Path("C:/") / "Users" / "e6105" / "Downloads" / "202101" / "config",
        "output_dir": BASE_DIR / "data" / "output",
    },
    "expected_summary": {
        "idmap section error": 34,
        "histTags ignore match": 1,
        "histTags noMatch": 15,
        "idmaps double": 0,
        "mpt": 1802,
        "hloc error": 18,
        "exPar error": 2,
        "intLoc missing": 0,
        "exPar missing": 346,
        "exLoc error": 5,
        "timeSeries error": 7,
        "validation error": 321,
        "par mismatch": 0,
        "locSet error": 337,
    },
    "paden": {
        "consistency_xlsx": "..\\data\\consistency.xlsx",
        "mpt_ignore_csv": "..\\data\\mpt_startenddate_total_pixml_transferdb_ignore.csv",
        "hist_tags_csv": "..\\data\\get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
        "fews_config": "D:\\WIS_6.0_ONTWIKKEL_202101\\FEWS_SA\\config",
        "csv_out": "..\\data\\csv",
    },
}

PATHS_nr3 = {
    "files": {
        "consistency_input_xlsx": BASE_DIR / "data" / "input" / "consistency_input.xlsx",
        "mpt_ignore_csv": BASE_DIR / "data" / "input" / "mpt_startenddate_total_pixml_transferdb_ignore.csv",
        "hist_tags_csv": BASE_DIR / "data" / "input" / "get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
    },
    "dirs": {
        # "fews_config": Path("D:") / "WIS_6.0_ONTWIKKEL_201902" / "FEWS_SA" / "config",
        "fews_config": Path("C:/") / "Users" / "e6105" / "Downloads" / "201902" / "config",
        "output_dir": BASE_DIR / "data" / "output",
    },
    "expected_summary": {
        "idmap section error": 36,
        "histTags ignore match": 0,
        "histTags noMatch": 69,
        "idmaps double": 0,
        "mpt": 1770,
        "pars missing": 1,
        "hloc error": 0,
        "exPar error": 2,
        "intLoc missing": 2,
        "exPar missing": 338,
        "exLoc error": 8,
        "timeSeries error": 62,
        "validation error": 273,
        "par mismatch": 0,
        "locSet error": 319,
    },
    "paden": {
        "consistency_xlsx": "..\\data\\consistency.xlsx",
        "mpt_ignore_csv": "..\\data\\mpt_startenddate_total_pixml_transferdb_ignore.csv",
        "hist_tags_csv": "..\\data\\get_series_startenddate_CAW_summary_total_sorted_20201013.csv",
        "fews_config": "D:\\WIS_6.0_ONTWIKKEL_201902\\FEWS_SA\\config",
        "csv_out": "..\\data\\csv",
    },
}

PATHS = PATHS_nr2

FIXED_SHEETS = [
    "histTag_ignore",
    "inhoudsopgave",
    "exLoc_ignore",
    "TS800_ignore",
    "xy_ignore",
]

LOCATIONS_SETS = {
    "hoofdlocaties": "OPVLWATER_HOOFDLOC",
    "sublocaties": "OPVLWATER_SUBLOC",
    "waterstandlocaties": "OPVLWATER_WATERSTANDEN_AUTO",
    "mswlocaties": "MSW_STATIONS",
    "peilschalen": "OPVLWATER_PEILSCHALEN",
}

IDMAP_FILES = [
    "IdOPVLWATER",
    "IdOPVLWATER_HYMOS",
    "IdHDSR_NSC",
    "IdOPVLWATER_WQ",
    "IdGrondwaterCAW",
]

IDMAP_SECTIONS = {
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
    "IdOPVLWATER_HYMOS": {
        "KUNSTWERKEN": [{"section_end": "<!--WATERSTANDSLOCATIES-->"}],
        "WATERSTANDLOCATIES": [{"section_start": "<!--WATERSTANDSLOCATIES-->", "section_end": "<!--OVERIG-->"}],
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
    "waterstand": ["HB.$", "HO.$", "H$"],
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
    {"internal": "H.R.", "external": "HR."},
    {"internal": "H.S.", "external": "HS."},
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

VALIDATION_RULES = {
    "sublocaties": [
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
    "hoofdlocaties": [
        {"parameter": "H.S.", "extreme_values": {"hmax": "HS1_HMAX", "hmin": "HS1_HMIN"}},
        {"parameter": "H2.S.", "extreme_values": {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}},
        {"parameter": "H3.S.", "extreme_values": {"hmax": "HS3_HMAX", "hmin": "HS3_HMIN"}},
    ],
    "waterstandlocaties": [
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
}


def check_constants():
    # check 1
    assert (
        BASE_DIR.name == "mptconfig_checker"
    ), f"BASE_DIR name ={BASE_DIR.name} should be project's root 'mptconfig_checker'"

    # check 2
    files = "files"
    dirs = "dirs"
    all_defined_paths = sorted([key for key in Paths.__dict__ if not key.startswith("__")])
    assert all_defined_paths == sorted(
        ["consistency_input_xlsx", "fews_config", "hist_tags_csv", "mpt_ignore_csv", "output_dir"]
    )
    for path_nt in [
        Paths.consistency_input_xlsx,
        Paths.fews_config,
        Paths.hist_tags_csv,
        Paths.mpt_ignore_csv,
        Paths.output_dir,
    ]:
        assert isinstance(path_nt.path, Path), f"path {path_nt.path} is not of type pathlib.Path"
        if not path_nt.must_exist:
            continue
        if path_nt.is_file:
            assert path_nt.path.is_file(), f"file does not exist with path={path_nt.path}"
        else:
            assert path_nt.path.is_dir(), f"dir does not exist with path={path_nt.path}"
