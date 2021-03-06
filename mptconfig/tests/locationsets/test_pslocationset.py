from mptconfig import constants
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2

import mptconfig.tests.fixtures


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_idmap_section_name_1_and_2 = ""
expected_name_1_and_2 = "peilschalen"
expected_csvfile_1_and_2 = "oppvlwater_peilschalen"
expected_fews_name_1_and_2 = "OPVLWATER_PEILSCHALEN"

expected_validation_attributes_1_and_2 = []

expected_validation_rules_1_and_2 = []

expected_csvfile_meta_1_and_2 = {
    "file": "oppvlwater_peilschalen",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "Locaties waterstanden",
    "toolTip": '<html>\n    <table id="details">\n      <tr>\n\t<td width="50" valign="top">ID</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%ID%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Naam</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%NAME%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Type</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">%DESCRIPTION%</td>\n      </tr>\n      <tr>\n\t<td width="50" valign="top">Foto</td>\n\t<td width="5" valign="top">:</td>\n\t<td width="200" valign="top">\n\t   <img src="file:$PHOTO_DIR$/Peilschaalfoto/%FOTO_ID%" border="0" width="300" height="300"/>\n\t</td>\n      </tr>\n    </table>\n</html>',  # noqa
    "startDateTime": "%START%",
    "endDateTime": "%EIND%",
    "x": "%X%",
    "y": "%Y%",
    "relation": [
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
    ],
    "attribute": [
        {"text": "%PEILBESLUI%", "id": "PEILBESLUIT"},
        {"text": "%RAYON%", "id": "RAYON"},
        {"text": "%FOTO_ID%", "id": "FOTO_ID"},
    ],
}

expected_attrib_files_1_and_2 = []


def test_pslocationset_1(patched_path_constants_1):
    psloc = constants.PeilschaalLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert psloc.fews_config.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_201902
    assert psloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert psloc.name == expected_name_1_and_2
    assert psloc.csv_filename == expected_csvfile_1_and_2
    assert psloc.fews_name == expected_fews_name_1_and_2
    assert psloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert psloc.validation_rules == expected_validation_rules_1_and_2
    assert psloc.csv_file_meta == expected_csvfile_meta_1_and_2
    assert psloc.attrib_files == expected_attrib_files_1_and_2


def test_pslocationset_2(patched_path_constants_2):
    psloc = constants.PeilschaalLocationSet(fews_config_path=constants.PathConstants.fews_config.value.path)
    assert psloc.fews_config.path == mptconfig.tests.fixtures.D_WIS_60_REFERENTIE_202002
    assert psloc.idmap_section_name == expected_idmap_section_name_1_and_2
    assert psloc.name == expected_name_1_and_2
    assert psloc.csv_filename == expected_csvfile_1_and_2
    assert psloc.fews_name == expected_fews_name_1_and_2
    assert psloc.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert psloc.validation_rules == expected_validation_rules_1_and_2
    assert psloc.csv_file_meta == expected_csvfile_meta_1_and_2
    assert psloc.attrib_files == expected_attrib_files_1_and_2
