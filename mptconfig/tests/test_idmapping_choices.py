from mptconfig.idmapping_choices import IntLocChoices


kw_hoofd1 = "KW123450"
kw_hoofd2 = "KW423410"
kw_sub1 = "KW123451"
kw_sub2 = "KW621001"
ow_loc1 = "OW123452"
ow_loc2 = "OW123452"
msw_loc1 = "KW763456"
msw_loc2 = "OW763456"


def test_is_kw_hoofd():
    assert IntLocChoices.is_kw_hoofd(int_loc=kw_hoofd1)
    assert IntLocChoices.is_kw_hoofd(int_loc=kw_hoofd2)
    assert not IntLocChoices.is_kw_hoofd(int_loc=kw_sub1)
    assert not IntLocChoices.is_kw_hoofd(int_loc=kw_sub2)
    assert not IntLocChoices.is_kw_hoofd(int_loc=ow_loc1)
    assert not IntLocChoices.is_kw_hoofd(int_loc=ow_loc2)
    assert not IntLocChoices.is_kw_hoofd(int_loc=msw_loc1)
    assert not IntLocChoices.is_kw_hoofd(int_loc=msw_loc2)


def test_is_kw_sub():
    assert IntLocChoices.is_kw_sub(int_loc=kw_sub1)
    assert IntLocChoices.is_kw_sub(int_loc=kw_sub2)
    assert not IntLocChoices.is_kw_sub(int_loc=kw_hoofd1)
    assert not IntLocChoices.is_kw_sub(int_loc=kw_hoofd2)
    assert not IntLocChoices.is_kw_sub(int_loc=ow_loc1)
    assert not IntLocChoices.is_kw_sub(int_loc=ow_loc2)
    assert not IntLocChoices.is_kw_sub(int_loc=msw_loc1)
    assert not IntLocChoices.is_kw_sub(int_loc=msw_loc2)


def test_is_ow():
    assert IntLocChoices.is_ow(int_loc=ow_loc1)
    assert IntLocChoices.is_ow(int_loc=ow_loc2)
    assert not IntLocChoices.is_ow(int_loc=kw_hoofd1)
    assert not IntLocChoices.is_ow(int_loc=kw_hoofd2)
    assert not IntLocChoices.is_ow(int_loc=kw_sub1)
    assert not IntLocChoices.is_ow(int_loc=kw_sub2)
    assert not IntLocChoices.is_ow(int_loc=msw_loc1)
    assert not IntLocChoices.is_ow(int_loc=msw_loc2)


def test_is_msw():
    assert IntLocChoices.is_msw(int_loc=msw_loc1)
    assert IntLocChoices.is_msw(int_loc=msw_loc1)
    assert not IntLocChoices.is_msw(int_loc=kw_hoofd1)
    assert not IntLocChoices.is_msw(int_loc=kw_hoofd2)
    assert not IntLocChoices.is_msw(int_loc=kw_sub1)
    assert not IntLocChoices.is_msw(int_loc=kw_sub2)
    assert not IntLocChoices.is_msw(int_loc=ow_loc1)
    assert not IntLocChoices.is_msw(int_loc=ow_loc2)
