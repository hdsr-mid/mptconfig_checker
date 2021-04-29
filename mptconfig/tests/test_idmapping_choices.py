from mptconfig.idmapping_choices import IntLocChoices


def test_is_kw_sub():
    assert IntLocChoices.is_kw_sub(int_loc="KW123451")
    assert not IntLocChoices.is_kw_sub(int_loc="KW123450")
    assert not IntLocChoices.is_kw_sub(int_loc="OW123450")
    assert not IntLocChoices.is_kw_sub(int_loc="OW123452")


def test_is_kw_hoofd():
    assert IntLocChoices.is_kw_hoofd(int_loc="KW123450")
    assert not IntLocChoices.is_kw_hoofd(int_loc="KW123451")
    assert not IntLocChoices.is_kw_hoofd(int_loc="OW123450")
    assert not IntLocChoices.is_kw_hoofd(int_loc="OW123452")


def test_is_ow():
    assert IntLocChoices.is_ow(int_loc="OW123450")
    assert IntLocChoices.is_ow(int_loc="OW123452")
    assert not IntLocChoices.is_ow(int_loc="KW123450")
    assert not IntLocChoices.is_ow(int_loc="KW123451")
