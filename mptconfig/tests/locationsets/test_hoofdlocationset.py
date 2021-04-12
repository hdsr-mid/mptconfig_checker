from mptconfig import constants
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2

import mptconfig.tests.fixtures


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_idmap_section_name_1_and_2 = "KUNSTWERKEN"
expected_name_1_and_2 = "hoofdlocaties"
expected_csvfile_1_and_2 = "oppvlwater_hoofdloc"
expected_fews_name_1_and_2 = "OPVLWATER_HOOFDLOC"


expected_validation_attributes_1_and_2 = ["HS1_HMAX", "HS1_HMIN", "HS2_HMAX", "HS2_HMIN", "HS3_HMAX", "HS3_HMIN"]

expected_validation_rules_1_and_2 = [
    {"parameter": "H.S.", "extreme_values": {"hmax": "HS1_HMAX", "hmin": "HS1_HMIN"}},
    {"parameter": "H2.S.", "extreme_values": {"hmax": "HS2_HMAX", "hmin": "HS2_HMIN"}},
    {"parameter": "H3.S.", "extreme_values": {"hmax": "HS3_HMAX", "hmin": "HS3_HMIN"}},
]

expected_csvfile_meta_1 = {
    "file": "oppvlwater_hoofdloc",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Hoofdlocaties oppervlaktewater",
    "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top"><img src="file:$PHOTO_DIR$/Kunstwerkfoto/%FOTO_ID%" border="0" width="300" height="300"/></td>\n    </tr>\n    </table>\n</html>',
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "z": "%Z%",
    "attribute": [
        {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%KOMPAS%", "id": "KOMPAS"},
        {"text": "%FOTO_ID%", "id": "FOTO_ID"},
        {"text": "%SCHEMA%", "id": "SCHEMA"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_hoofdloc_parameters.csv",
            "id": "%LOC_ID%",
            "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
        },
        {
            "csvFile": "oppvlwater_hoofdloc_validations.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%kunstvalidatie_streef1%", "id": "kunstvalidatie_streef1"},
                {"text": "%kunstvalidatie_streef2%", "id": "kunstvalidatie_streef2"},
                {"text": "%kunstvalidatie_streef3%", "id": "kunstvalidatie_streef3"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef1.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS1_HMAX%", "id": "HS1_HMAX"}, {"number": "%HS1_HMIN%", "id": "HS1_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS2_HMAX%", "id": "HS2_HMAX"}, {"number": "%HS2_HMIN%", "id": "HS2_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef3.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS3_HMAX%", "id": "HS3_HMAX"}, {"number": "%HS3_HMIN%", "id": "HS3_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kentermeetdata.csv",
            "id": "%LOC_ID%",
            "attribute": [{"text": "%KENTER_EAN%", "id": "KENTER_EAN"}, {"text": "%METER_ID%", "id": "METER_ID"}],
        },
    ],
}
expected_csvfile_meta_2 = {
    "file": "oppvlwater_hoofdloc",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Hoofdlocaties oppervlaktewater",
    "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top"><img src="file:$PHOTO_DIR$/Kunstwerkfoto/%FOTO_ID%" border="0" width="300" height="300"/></td>\n    </tr>\n    </table>\n</html>',  # noqa
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "z": "%Z%",
    "attribute": [
        {"text": "%ALLE_TYPES%", "id": "ALLE_TYPES"},
        {"text": "%SYSTEEM%", "id": "HOOFDSYSTEEM"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%KOMPAS%", "id": "KOMPAS"},
        {"text": "%FOTO_ID%", "id": "FOTO_ID"},
        {"text": "%SCHEMA%", "id": "SCHEMA"},
    ],
    "attributeFile": [
        {
            "csvFile": "oppvlwater_hoofdloc_parameters.csv",
            "id": "%LOC_ID%",
            "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
        },
        {
            "csvFile": "oppvlwater_hoofdloc_validations.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%kunstvalidatie_streef1%", "id": "kunstvalidatie_streef1"},
                {"text": "%kunstvalidatie_streef2%", "id": "kunstvalidatie_streef2"},
                {"text": "%kunstvalidatie_streef3%", "id": "kunstvalidatie_streef3"},
            ],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef1.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS1_HMAX%", "id": "HS1_HMAX"}, {"number": "%HS1_HMIN%", "id": "HS1_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef2.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS2_HMAX%", "id": "HS2_HMAX"}, {"number": "%HS2_HMIN%", "id": "HS2_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kunstvalidatie_streef3.csv",
            "id": "%LOC_ID%",
            "startDateTime": "%STARTDATE%",
            "endDateTime": "%ENDDATE%",
            "attribute": [{"number": "%HS3_HMAX%", "id": "HS3_HMAX"}, {"number": "%HS3_HMIN%", "id": "HS3_HMIN"}],
        },
        {
            "csvFile": "oppvlwater_kentermeetdata.csv",
            "id": "%LOC_ID%",
            "attribute": [
                {"text": "%KENTER_EAN%", "id": "EAN"},
                {"text": "%KENTER_EAN%", "id": "KENTER_EAN"},
                {"text": "%METER_ID%", "id": "METER_ID"},
            ],
        },
    ],
}

expected_attrib_files_1 = [
    {
        "csvFile": "oppvlwater_hoofdloc_parameters.csv",
        "id": "%LOC_ID%",
        "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
    },
    {
        "csvFile": "oppvlwater_hoofdloc_validations.csv",
        "id": "%LOC_ID%",
        "attribute": [
            {"text": "%kunstvalidatie_streef1%", "id": "kunstvalidatie_streef1"},
            {"text": "%kunstvalidatie_streef2%", "id": "kunstvalidatie_streef2"},
            {"text": "%kunstvalidatie_streef3%", "id": "kunstvalidatie_streef3"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_streef1.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HS1_HMAX%", "id": "HS1_HMAX"}, {"number": "%HS1_HMIN%", "id": "HS1_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_streef2.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HS2_HMAX%", "id": "HS2_HMAX"}, {"number": "%HS2_HMIN%", "id": "HS2_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_streef3.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HS3_HMAX%", "id": "HS3_HMAX"}, {"number": "%HS3_HMIN%", "id": "HS3_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kentermeetdata.csv",
        "id": "%LOC_ID%",
        "attribute": [{"text": "%KENTER_EAN%", "id": "KENTER_EAN"}, {"text": "%METER_ID%", "id": "METER_ID"}],
    },
]

expected_attrib_files_2 = [
    {
        "csvFile": "oppvlwater_hoofdloc_parameters.csv",
        "id": "%LOC_ID%",
        "attribute": {"text": "%PARAMETERS%", "id": "PARAMETERS"},
    },
    {
        "csvFile": "oppvlwater_hoofdloc_validations.csv",
        "id": "%LOC_ID%",
        "attribute": [
            {"text": "%kunstvalidatie_streef1%", "id": "kunstvalidatie_streef1"},
            {"text": "%kunstvalidatie_streef2%", "id": "kunstvalidatie_streef2"},
            {"text": "%kunstvalidatie_streef3%", "id": "kunstvalidatie_streef3"},
        ],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_streef1.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HS1_HMAX%", "id": "HS1_HMAX"}, {"number": "%HS1_HMIN%", "id": "HS1_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_streef2.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HS2_HMAX%", "id": "HS2_HMAX"}, {"number": "%HS2_HMIN%", "id": "HS2_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kunstvalidatie_streef3.csv",
        "id": "%LOC_ID%",
        "startDateTime": "%STARTDATE%",
        "endDateTime": "%ENDDATE%",
        "attribute": [{"number": "%HS3_HMAX%", "id": "HS3_HMAX"}, {"number": "%HS3_HMIN%", "id": "HS3_HMIN"}],
    },
    {
        "csvFile": "oppvlwater_kentermeetdata.csv",
        "id": "%LOC_ID%",
        "attribute": [
            {"text": "%KENTER_EAN%", "id": "EAN"},
            {"text": "%KENTER_EAN%", "id": "KENTER_EAN"},
            {"text": "%METER_ID%", "id": "METER_ID"},
        ],
    },
]


def test_hoofdlocationset_1(patched_path_constants_1):
    hoofdloc = constants.HoofdLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert hoofdloc.fews_config.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_201902
    assert hoofdloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert hoofdloc.name == expected_name_1_and_2
    assert hoofdloc.csv_filename == expected_csvfile_1_and_2
    assert hoofdloc.fews_name == expected_fews_name_1_and_2
    assert hoofdloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert hoofdloc.validation_rules == expected_validation_rules_1_and_2
    assert hoofdloc.csv_file_meta == expected_csvfile_meta_1
    assert hoofdloc.attrib_files == expected_attrib_files_1


def test_hoofdlocationset_2(patched_path_constants_2):
    hoofdloc = constants.HoofdLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert hoofdloc.fews_config.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_202002
    assert hoofdloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert hoofdloc.name == expected_name_1_and_2
    assert hoofdloc.csv_filename == expected_csvfile_1_and_2
    assert hoofdloc.fews_name == expected_fews_name_1_and_2
    assert hoofdloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert hoofdloc.validation_rules == expected_validation_rules_1_and_2
    assert hoofdloc.csv_file_meta == expected_csvfile_meta_2
    assert hoofdloc.attrib_files == expected_attrib_files_2
