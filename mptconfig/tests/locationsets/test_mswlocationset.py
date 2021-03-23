from mptconfig.constants import mswlocationset
from mptconfig.tests.fixtures import patched_path_constants_1
from mptconfig.tests.fixtures import patched_path_constants_2


# silence flake8 errors
_patched_path_constants_1 = patched_path_constants_1
_patched_path_constants_2 = patched_path_constants_2

expected_idmap_section_name_1_and_2 = ""
expected_name_1_and_2 = "mswlocaties"
expected_csvfile_1_and_2 = "msw_stations"
expected_fews_name_1_and_2 = "MSW_STATIONS"

expected_validation_attributes_1_and_2 = []

expected_validation_rules_1_and_2 = []

expected_csvfile_meta_1_and_2 = {
    "file": "msw_stations",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "MSW-station",
    "x": "%X%",
    "y": "%Y%",
    "relation": [
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
    ],
    "attribute": {"text": "%PARS%", "id": "PARS"},
}

expected_attrib_files_1_and_2 = None


def test_mswlocationset_1(patched_path_constants_1):
    assert mswlocationset.idmap_section_name == expected_idmap_section_name_1_and_2
    assert mswlocationset.name == expected_name_1_and_2
    assert mswlocationset.csvfile == expected_csvfile_1_and_2
    assert mswlocationset.fews_name == expected_fews_name_1_and_2
    assert mswlocationset.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert mswlocationset.validation_rules == expected_validation_rules_1_and_2
    assert mswlocationset.csvfile_meta == expected_csvfile_meta_1_and_2
    # TODO: find out why keyerror
    #  attribute_files = self.csvfile_meta["attributeFile"]
    #  KeyError: 'attributeFile'
    #  assert mswlocationset.attrib_files == expected_attrib_files_1_and_2


def test_mswlocationset_2(patched_path_constants_2):
    assert mswlocationset.idmap_section_name == expected_idmap_section_name_1_and_2
    assert mswlocationset.name == expected_name_1_and_2
    assert mswlocationset.csvfile == expected_csvfile_1_and_2
    assert mswlocationset.fews_name == expected_fews_name_1_and_2
    assert mswlocationset.get_validation_attributes(int_pars=None) == expected_validation_attributes_1_and_2
    assert mswlocationset.validation_rules == expected_validation_rules_1_and_2
    assert mswlocationset.csvfile_meta == expected_csvfile_meta_1_and_2
    # TODO: find out why keyerror
    #  attribute_files = self.csvfile_meta["attributeFile"]
    #  KeyError: 'attributeFile'
    #  assert mswlocationset.attrib_files == expected_attrib_files_1_and_2
