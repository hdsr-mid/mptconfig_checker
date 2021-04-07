from mptconfig import constants
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2
from pathlib import Path


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_idmap_section_name_1_and_2 = "KUNSTWERKEN"
expected_name_1_and_2 = "sublocaties"
expected_csvfile_1_and_2 = "oppvlwater_subloc"
expected_fews_name_1_and_2 = "OPVLWATER_SUBLOC"

expected_validation_attributes_1_and_2 = [
    "HR1_HMAX",
    "HR1_HMIN",
    "HR2_HMAX",
    "HR2_HMIN",
    "HR3_HMAX",
    "HR3_HMIN",
    "Q_HMAX",
    "Q_SMAX",
    "Q_SMIN",
    "Q_HMIN",
    "Q_HMAX",
    "Q_SMAX",
    "Q_SMIN",
    "Q_HMIN",
    "FRQ_HMAX",
    "FRQ_HMIN",
    "HEF_HMAX",
    "HEF_HMIN",
    "PERC_HMAX",
    "PERC_SMAX",
    "PERC_SMIN",
    "PERC_HMIN",
    "PERC2_HMAX",
    "PERC2_SMAX",
    "PERC2_SMIN",
    "PERC2_HMIN",
    "TT_HMAX",
    "TT_HMIN",
]

expected_validation_rules_1_and_2 = [
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
]

expected_csvfile_meta_1_and_2 = {
    "file": "oppvlwater_subloc",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Sublocaties oppervlaktewater",
    "parentLocationId": "%PAR_ID%",
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "relation": [
        {"relatedLocationId": "%HBOV%", "id": "HBOV"},
        {"relatedLocationId": "%HBEN%", "id": "HBEN"},
        {"relatedLocationId": "%HBOVPS%", "id": "HBOVPS"},
        {"relatedLocationId": "%HBENPS%", "id": "HBENPS"},
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
        {"relatedLocationId": "%B_VAN%", "id": "B_VAN"},
        {"relatedLocationId": "%B_NAAR%", "id": "B_NAAR"},
        {"relatedLocationId": "%AFGB_VAN%", "id": "AFGB_VAN"},
        {"relatedLocationId": "%AFGB_NAAR%", "id": "AFGB_NAAR"},
    ],
    "attribute": [
        {"text": "%LOC_NAME%", "id": "LOC_NAME"},
        {"text": "%QNORM%", "id": "QNORM"},
        {"text": "%TYPE%", "id": "TYPE"},
        {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
        {"text": "%FUNCTIE%", "id": "FUNCTIE"},
        {"text": "%AKKOORD%", "id": "WATERAKKOORD"},
        {"text": "%BALANS%", "id": "WATERBALANS"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%KOMPAS%", "id": "KOMPAS"},
        {"text": "%HBOV%", "id": "HBOV"},
        {"text": "%HBEN%", "id": "HBEN"},
        {"text": "%AFGB_NAAR%", "id": "AFGB_NAAR"},
        {"text": "%AFGB_VAN%", "id": "AFGB_VAN"},
        {"description": "Dit attribuut wordt in de filters gebruikt", "boolean": "%SWM%", "id": "SWM"},
        {"boolean": "%NWW-MDV%", "id": "SWMGEBIED_NWW-MDV"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_subloc_parameters.csv",
            "id": "%LOC_ID%",
            "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
        },
        {
            "csvFile": "oppvlwater_subloc_validations.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%kunstvalidatie_freq%", "id": "kunstvalidatie_freq"},
                {"text": "%kunstvalidatie_kroos%", "id": "kunstvalidatie_kroos"},
                {"text": "%kunstvalidatie_kruinh%", "id": "kunstvalidatie_kruinh"},
                {"text": "%kunstvalidatie_schuifp%", "id": "kunstvalidatie_schuifp"},
                {"text": "%kunstvalidatie_schuifp2%", "id": "kunstvalidatie_schuifp2"},
                {"text": "%kunstvalidatie_stuur1%", "id": "kunstvalidatie_stuur1"},
                {"text": "%kunstvalidatie_stuur2%", "id": "kunstvalidatie_stuur2"},
                {"text": "%kunstvalidatie_stuur3%", "id": "kunstvalidatie_stuur3"},
            ],
        },
        {
            "csvFile": "oppvlwater_subloc_relatie_swm_arknzk.csv",
            "id": "%LOC_ID%",
            "checkForContinuousPeriod": "false",
            "relation": {"relatedLocationId": "%ACTUEEL%", "id": "SWMGEBIED"},
            "attribute": {"text": "%ACTUEEL%", "id": "SWMGEBIED_NZK-ARK"},
        },
        {
            "description": "GEEN TIJDSAFHANKELIJKHEID GEBRUIKEN HIER VOORLOPIG",
            "csvFile": "oppvlwater_subloc_relatie_debietmeter.csv",
            "id": "%LOC_ID%",
            "relation": {"relatedLocationId": "%DEBIETMETER%", "id": "DEBIETMETER"},
            "attribute": {"text": "DEBIETMETER", "id": "DEBIETMETER"},
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_debiet.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%Q_SMAX%", "id": "Q_SMAX"},
                {"number": "%Q_SMIN%", "id": "Q_SMIN"},
                {"number": "%Q_HMAX%", "id": "Q_HMAX"},
                {"number": "%Q_HMIN%", "id": "Q_HMIN"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_freq.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%FRQ_HMAX%", "id": "FRQ_HMAX"},
                {"number": "%FRQ_HMIN%", "id": "FRQ_HMIN"},
                {"number": "%FRQ_RRRF%", "id": "FRQ_RRRF"},
                {"number": "%FRQ_RTS%", "id": "FRQ_RTS"},
                {"number": "%FRQ_TPS%", "id": "FRQ_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_hefh.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%HEF_HMAX%", "id": "HEF_HMAX"},
                {"number": "%HEF_HMIN%", "id": "HEF_HMIN"},
                {"number": "%HEF_RRRF%", "id": "HEF_RRRF"},
                {"number": "%HEF_SARE%", "id": "HEF_SARE"},
                {"number": "%HEF_SAPE%", "id": "HEF_SAPE"},
                {"number": "%HEF_RTS%", "id": "HEF_RTS"},
                {"number": "%HEF_TPS%", "id": "HEF_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_kruinh.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%KR_SMAX%", "id": "KR_SMAX"},
                {"number": "%KR_SMIN%", "id": "KR_SMIN"},
                {"number": "%KR_HMAX%", "id": "KR_HMAX"},
                {"number": "%KR_HMIN%", "id": "KR_HMIN"},
                {"number": "%KR_RRRF%", "id": "KR_RRRF"},
                {"number": "%KR_SARE%", "id": "KR_SARE"},
                {"number": "%KR_SAPE%", "id": "KR_SAPE"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_schuifp.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%PERC_HMAX%", "id": "PERC_HMAX"},
                {"number": "%PERC_HMIN%", "id": "PERC_HMIN"},
                {"number": "%PERC_SMAX%", "id": "PERC_SMAX"},
                {"number": "%PERC_SMIN%", "id": "PERC_SMIN"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_schuifp2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%PERC2_HMAX%", "id": "PERC2_HMAX"},
                {"number": "%PERC2_HMIN%", "id": "PERC2_HMIN"},
                {"number": "%PERC2_SMAX%", "id": "PERC2_SMAX"},
                {"number": "%PERC2_SMIN%", "id": "PERC2_SMIN"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_toert.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%TT_HMAX%", "id": "TT_HMAX"},
                {"number": "%TT_HMIN%", "id": "TT_HMIN"},
                {"number": "%TT_RRRF%", "id": "TT_RRRF"},
                {"number": "%TT_SARE%", "id": "TT_SARE"},
                {"number": "%TT_SAPE%", "id": "TT_SAPE"},
                {"number": "%TT_RTS%", "id": "TT_RTS"},
                {"number": "%TT_TPS%", "id": "TT_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_kroos.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [
                {"number": "%HW_SMAX%", "id": "HW_SMAX"},
                {"number": "%HW_SMIN%", "id": "HW_SMIN"},
                {"number": "%HO_SMAX%", "id": "HO_SMAX"},
                {"number": "%HO_SMIN%", "id": "HO_SMIN"},
                {"number": "%HZ_SMAX%", "id": "HZ_SMAX"},
                {"number": "%HZ_SMIN%", "id": "HZ_SMIN"},
                {"number": "%H_HMAX%", "id": "H_HMAX"},
                {"number": "%H_HMIN%", "id": "H_HMIN"},
                {"number": "%H_RRRF%", "id": "H_RRRF"},
                {"number": "%H_SARE%", "id": "H_SARE"},
                {"number": "%H_SAPE%", "id": "H_SAPE"},
                {"number": "%H_RTS%", "id": "H_RTS"},
                {"number": "%H_TPS%", "id": "H_TPS"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_stuur1.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HR1_HMAX%", "id": "HR1_HMAX"}, {"number": "%HR1_HMIN%", "id": "HR1_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_stuur2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HR2_HMAX%", "id": "HR2_HMAX"}, {"number": "%HR2_HMIN%", "id": "HR2_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_stuur3.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HR3_HMAX%", "id": "HR3_HMAX"}, {"number": "%HR3_HMIN%", "id": "HR3_HMIN"}],
        },
        {
            "csvFile": "herberekeningDebietenLocsets.csv",
            "id": "%locid%",
            "relation": [
                {"relatedLocationId": "%totaal_plus%", "id": "totaal_plus"},
                {"relatedLocationId": "%totaal_min%", "id": "totaal_min"},
            ],
            "attribute": [{"text": "%formule%", "id": "formule"}, {"text": "%keuze_formule%", "id": "keuze_formule"}],
        },
        {
            "csvFile": "herberekeningDebieten.csv",
            "id": "%locid%",
            "dateTimePattern": "yyyy-MM-dd",
            "startDateTime": "%startdate%",
            "endDateTime": "%enddate%",
            "attribute": [
                {"number": "%breedte%", "id": "breedte"},
                {"number": "%cc%", "id": "cc"},
                {"number": "%cd%", "id": "cd"},
                {"number": "%coefficient_a%", "id": "coefficient_a"},
                {"number": "%coefficient_b%", "id": "coefficient_b"},
                {"number": "%coefficient_c%", "id": "coefficient_c"},
                {"number": "%cv%", "id": "cv"},
                {"number": "%diameter%", "id": "diameter"},
                {"number": "%drempelhoogte%", "id": "drempelhoogte"},
                {"number": "%keuze_afsluitertype%", "id": "keuze_afsluitertype"},
                {"number": "%lengte%", "id": "lengte"},
                {"number": "%max_frequentie%", "id": "max_frequentie"},
                {"number": "%max_schuif%", "id": "max_schuif"},
                {"number": "%ontwerp_capaciteit%", "id": "ontwerp_capaciteit"},
                {"number": "%sw%", "id": "sw"},
                {"number": "%tastpunt%", "id": "tastpunt"},
                {"number": "%vulpunt%", "id": "vulpunt"},
                {"number": "%wandruwheid%", "id": "wandruwheid"},
                {"number": "%xi_extra%", "id": "xi_extra"},
                {"number": "%xi_intree%", "id": "xi_intree"},
                {"number": "%xi_uittree%", "id": "xi_uittree"},
                {"number": "%vaste_frequentie%", "id": "vaste_frequentie"},
            ],
        },
        {
            "csvFile": "herberekeningDebieten_h.csv",
            "id": "%locid%",
            "attribute": [
                {"number": "%bovenpeil%", "id": "bovenpeil"},
                {"number": "%benedenpeil%", "id": "benedenpeil"},
            ],
        },
    ],
}

expected_attrib_files_1_and_2 = [
    {
        "csvFile": "oppvlwater_subloc_parameters.csv",
        "id": "%LOC_ID%",
        "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
    },
    {
        "csvFile": "oppvlwater_subloc_validations.csv",
        "id": "%LOC_ID%",
        "attribute": [
            {"text": "%kunstvalidatie_freq%", "id": "kunstvalidatie_freq"},
            {"text": "%kunstvalidatie_kroos%", "id": "kunstvalidatie_kroos"},
            {"text": "%kunstvalidatie_kruinh%", "id": "kunstvalidatie_kruinh"},
            {"text": "%kunstvalidatie_schuifp%", "id": "kunstvalidatie_schuifp"},
            {"text": "%kunstvalidatie_schuifp2%", "id": "kunstvalidatie_schuifp2"},
            {"text": "%kunstvalidatie_stuur1%", "id": "kunstvalidatie_stuur1"},
            {"text": "%kunstvalidatie_stuur2%", "id": "kunstvalidatie_stuur2"},
            {"text": "%kunstvalidatie_stuur3%", "id": "kunstvalidatie_stuur3"},
        ],
    },
    {
        "csvFile": "oppvlwater_subloc_relatie_swm_arknzk.csv",
        "id": "%LOC_ID%",
        "checkForContinuousPeriod": "false",
        "relation": {"relatedLocationId": "%ACTUEEL%", "id": "SWMGEBIED"},
        "attribute": {"text": "%ACTUEEL%", "id": "SWMGEBIED_NZK-ARK"},
    },
    {
        "description": "GEEN TIJDSAFHANKELIJKHEID GEBRUIKEN HIER VOORLOPIG",
        "csvFile": "oppvlwater_subloc_relatie_debietmeter.csv",
        "id": "%LOC_ID%",
        "relation": {"relatedLocationId": "%DEBIETMETER%", "id": "DEBIETMETER"},
        "attribute": {"text": "DEBIETMETER", "id": "DEBIETMETER"},
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_debiet.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%Q_SMAX%", "id": "Q_SMAX"},
            {"number": "%Q_SMIN%", "id": "Q_SMIN"},
            {"number": "%Q_HMAX%", "id": "Q_HMAX"},
            {"number": "%Q_HMIN%", "id": "Q_HMIN"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_freq.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%FRQ_HMAX%", "id": "FRQ_HMAX"},
            {"number": "%FRQ_HMIN%", "id": "FRQ_HMIN"},
            {"number": "%FRQ_RRRF%", "id": "FRQ_RRRF"},
            {"number": "%FRQ_RTS%", "id": "FRQ_RTS"},
            {"number": "%FRQ_TPS%", "id": "FRQ_TPS"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_hefh.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%HEF_HMAX%", "id": "HEF_HMAX"},
            {"number": "%HEF_HMIN%", "id": "HEF_HMIN"},
            {"number": "%HEF_RRRF%", "id": "HEF_RRRF"},
            {"number": "%HEF_SARE%", "id": "HEF_SARE"},
            {"number": "%HEF_SAPE%", "id": "HEF_SAPE"},
            {"number": "%HEF_RTS%", "id": "HEF_RTS"},
            {"number": "%HEF_TPS%", "id": "HEF_TPS"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_kruinh.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%KR_SMAX%", "id": "KR_SMAX"},
            {"number": "%KR_SMIN%", "id": "KR_SMIN"},
            {"number": "%KR_HMAX%", "id": "KR_HMAX"},
            {"number": "%KR_HMIN%", "id": "KR_HMIN"},
            {"number": "%KR_RRRF%", "id": "KR_RRRF"},
            {"number": "%KR_SARE%", "id": "KR_SARE"},
            {"number": "%KR_SAPE%", "id": "KR_SAPE"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_schuifp.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%PERC_HMAX%", "id": "PERC_HMAX"},
            {"number": "%PERC_HMIN%", "id": "PERC_HMIN"},
            {"number": "%PERC_SMAX%", "id": "PERC_SMAX"},
            {"number": "%PERC_SMIN%", "id": "PERC_SMIN"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_schuifp2.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%PERC2_HMAX%", "id": "PERC2_HMAX"},
            {"number": "%PERC2_HMIN%", "id": "PERC2_HMIN"},
            {"number": "%PERC2_SMAX%", "id": "PERC2_SMAX"},
            {"number": "%PERC2_SMIN%", "id": "PERC2_SMIN"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_toert.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%TT_HMAX%", "id": "TT_HMAX"},
            {"number": "%TT_HMIN%", "id": "TT_HMIN"},
            {"number": "%TT_RRRF%", "id": "TT_RRRF"},
            {"number": "%TT_SARE%", "id": "TT_SARE"},
            {"number": "%TT_SAPE%", "id": "TT_SAPE"},
            {"number": "%TT_RTS%", "id": "TT_RTS"},
            {"number": "%TT_TPS%", "id": "TT_TPS"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_kroos.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [
            {"number": "%HW_SMAX%", "id": "HW_SMAX"},
            {"number": "%HW_SMIN%", "id": "HW_SMIN"},
            {"number": "%HO_SMAX%", "id": "HO_SMAX"},
            {"number": "%HO_SMIN%", "id": "HO_SMIN"},
            {"number": "%HZ_SMAX%", "id": "HZ_SMAX"},
            {"number": "%HZ_SMIN%", "id": "HZ_SMIN"},
            {"number": "%H_HMAX%", "id": "H_HMAX"},
            {"number": "%H_HMIN%", "id": "H_HMIN"},
            {"number": "%H_RRRF%", "id": "H_RRRF"},
            {"number": "%H_SARE%", "id": "H_SARE"},
            {"number": "%H_SAPE%", "id": "H_SAPE"},
            {"number": "%H_RTS%", "id": "H_RTS"},
            {"number": "%H_TPS%", "id": "H_TPS"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_stuur1.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HR1_HMAX%", "id": "HR1_HMAX"}, {"number": "%HR1_HMIN%", "id": "HR1_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_stuur2.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HR2_HMAX%", "id": "HR2_HMAX"}, {"number": "%HR2_HMIN%", "id": "HR2_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_stuur3.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HR3_HMAX%", "id": "HR3_HMAX"}, {"number": "%HR3_HMIN%", "id": "HR3_HMIN"}],
    },
    {
        "csvFile": "herberekeningDebietenLocsets.csv",
        "id": "%locid%",
        "relation": [
            {"relatedLocationId": "%totaal_plus%", "id": "totaal_plus"},
            {"relatedLocationId": "%totaal_min%", "id": "totaal_min"},
        ],
        "attribute": [{"text": "%formule%", "id": "formule"}, {"text": "%keuze_formule%", "id": "keuze_formule"}],
    },
    {
        "csvFile": "herberekeningDebieten.csv",
        "id": "%locid%",
        "dateTimePattern": "yyyy-MM-dd",
        "startDateTime": "%startdate%",
        "endDateTime": "%enddate%",
        "attribute": [
            {"number": "%breedte%", "id": "breedte"},
            {"number": "%cc%", "id": "cc"},
            {"number": "%cd%", "id": "cd"},
            {"number": "%coefficient_a%", "id": "coefficient_a"},
            {"number": "%coefficient_b%", "id": "coefficient_b"},
            {"number": "%coefficient_c%", "id": "coefficient_c"},
            {"number": "%cv%", "id": "cv"},
            {"number": "%diameter%", "id": "diameter"},
            {"number": "%drempelhoogte%", "id": "drempelhoogte"},
            {"number": "%keuze_afsluitertype%", "id": "keuze_afsluitertype"},
            {"number": "%lengte%", "id": "lengte"},
            {"number": "%max_frequentie%", "id": "max_frequentie"},
            {"number": "%max_schuif%", "id": "max_schuif"},
            {"number": "%ontwerp_capaciteit%", "id": "ontwerp_capaciteit"},
            {"number": "%sw%", "id": "sw"},
            {"number": "%tastpunt%", "id": "tastpunt"},
            {"number": "%vulpunt%", "id": "vulpunt"},
            {"number": "%wandruwheid%", "id": "wandruwheid"},
            {"number": "%xi_extra%", "id": "xi_extra"},
            {"number": "%xi_intree%", "id": "xi_intree"},
            {"number": "%xi_uittree%", "id": "xi_uittree"},
            {"number": "%vaste_frequentie%", "id": "vaste_frequentie"},
        ],
    },
    {
        "csvFile": "herberekeningDebieten_h.csv",
        "id": "%locid%",
        "attribute": [{"number": "%bovenpeil%", "id": "bovenpeil"}, {"number": "%benedenpeil%", "id": "benedenpeil"}],
    },
]


def test_sublocationset_1(patched_path_constants_1):
    subloc = constants.SubLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert subloc.fews_config.path == Path("D:WIS_6.0_ONTWIKKEL_201902_MPTCHECKER_TEST_INPUT/FEWS_SA/config")
    assert subloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert subloc.name == expected_name_1_and_2
    assert subloc.csv_filename == expected_csvfile_1_and_2
    assert subloc.fews_name == expected_fews_name_1_and_2
    assert subloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert subloc.validation_rules == expected_validation_rules_1_and_2
    assert subloc.csv_file_meta == expected_csvfile_meta_1_and_2
    assert subloc.attrib_files == expected_attrib_files_1_and_2


def test_sublocationset_2(patched_path_constants_2):
    subloc = constants.SubLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert subloc.fews_config.path == Path("D:WIS_6.0_ONTWIKKEL_202002_MPTCHECKER_TEST_INPUT/FEWS_SA/config")
    assert subloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert subloc.name == expected_name_1_and_2
    assert subloc.csv_filename == expected_csvfile_1_and_2
    assert subloc.fews_name == expected_fews_name_1_and_2
    assert subloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert subloc.validation_rules == expected_validation_rules_1_and_2
    assert subloc.csv_file_meta == expected_csvfile_meta_1_and_2
    assert subloc.attrib_files == expected_attrib_files_1_and_2
