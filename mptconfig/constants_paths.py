from collections import namedtuple
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
PathNamedTuple = namedtuple("Paths", ["is_file", "should_exist", "path", "description"])


class PathConstants1:
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


class PathConstants2:
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
    "validation error": 321,
    "par mismatch": 0,
    "locSet error": 335,
}


class PathConstants3:
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


PathConstants = PathConstants3
EXPECTED_SUMMARY = EXPECTED_SUMMARY3
