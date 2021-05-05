from mptconfig.constants import ValidationLogic


def test_get_validation_logic():
    # ensure [hmin <= smin < smax <= hmax]
    assert ValidationLogic.get_hloc_sloc_validation_logic() == [
        ("hmin", "<=", "smin"),
        ("hmin", "<", "smax"),
        ("hmin", "<", "hmax"),
        ("smin", "<", "smax"),
        ("smin", "<", "hmax"),
        ("smax", "<=", "hmax"),
    ]

    # ensure [hmin <= smin < smax <= hmax] combined with [WIN <= OV <= ZOM]
    assert ValidationLogic.get_wloc_validation_logic() == [
        ("hmin", "<=", "smin_win"),
        ("hmin", "<=", "smin_ov"),
        ("hmin", "<=", "smin_zom"),
        ("hmin", "<", "smax_win"),
        ("hmin", "<", "smax_ov"),
        ("hmin", "<", "smax_zom"),
        ("hmin", "<", "hmax"),
        ("smin_win", "<=", "smin_ov"),
        ("smin_win", "<=", "smin_zom"),
        ("smin_win", "<", "smax_win"),
        ("smin_win", "<", "smax_ov"),
        ("smin_win", "<", "smax_zom"),
        ("smin_win", "<", "hmax"),
        ("smin_ov", "<=", "smin_zom"),
        ("smin_ov", "<", "smax_win"),
        ("smin_ov", "<", "smax_ov"),
        ("smin_ov", "<", "smax_zom"),
        ("smin_ov", "<", "hmax"),
        ("smin_zom", "<", "smax_win"),
        ("smin_zom", "<", "smax_ov"),
        ("smin_zom", "<", "smax_zom"),
        ("smin_zom", "<", "hmax"),
        ("smax_win", "<=", "smax_ov"),
        ("smax_win", "<=", "smax_zom"),
        ("smax_win", "<=", "hmax"),
        ("smax_ov", "<=", "smax_zom"),
        ("smax_ov", "<=", "hmax"),
        ("smax_zom", "<=", "hmax"),
    ]
