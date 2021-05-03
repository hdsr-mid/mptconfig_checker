"""
typical IdOPVLWATER.xml content has 4 "columns":
    <map externalLocation="610" externalParameter="Q1" internalLocation="KW761001" internalParameter="Q.G.0"/>  # noqa
    <map externalLocation="612" externalParameter="HB1" internalLocation="OW761202" internalParameter="H.G.0"/>
    <map externalLocation="1001" externalParameter="FQ1" internalLocation="KW100111" internalParameter="F.0"/>
    <map externalLocation="1001" externalParameter="HS1" internalLocation="KW100110" internalParameter="H.S.0"/>
Below we defined 4 classes:
    externalLocation -> ExLocChoices
    externalParameter -> ExparChoices
    internalLocation -> IntLocChoices
    internalParameter -> IntParChoices
"""

from enum import Enum

import re


class ExLocChoices(Enum):
    pass


class ExParChoices(Enum):
    pass


class IntLocChoices(Enum):

    # in general (hoofd, sub, ow):
    # 1. first digit not 0, so [1-9]
    # 2. second to fifth digit = [0-9]
    # 3. sixth digit:
    #   KW hoofd: 0
    #   KW sub: [1-9]
    #   OW: [0-9]

    # in general msw:
    # 1. first two digits are 76
    # 2. second to sixth digit [0-9]

    kw_hoofd = "^KW[1-9][0-9]{4}0$"
    kw_sub = "^KW[1-9][0-9]{4}[1-9]$"
    ow = "^OW[1-9][0-9]{5}$"
    msw = "^(O|K)W76[0-9]{4}$"

    @classmethod
    def is_kw_hoofd(cls, int_loc: str) -> bool:
        """Hoofdlocations start with 'KW' followed by 6 digits with the last being 0, eg. KW123450"""
        assert isinstance(int_loc, str)
        if cls.is_msw(int_loc=int_loc):
            return False
        return bool(re.match(pattern=cls.kw_hoofd.value, string=int_loc))

    @classmethod
    def is_kw_sub(cls, int_loc: str) -> bool:
        """Sublocations start with 'KW' followed by 6 digits with the last not being 0, eg. KW123451"""
        assert isinstance(int_loc, str)
        if cls.is_msw(int_loc=int_loc):
            return False
        return bool(re.match(pattern=cls.kw_sub.value, string=int_loc))

    @classmethod
    def is_ow(cls, int_loc: str) -> bool:
        """OW locations start with 'OW' followed by 6 digits, eg. OW123456"""
        assert isinstance(int_loc, str)
        if cls.is_msw(int_loc=int_loc):
            return False
        return bool(re.match(pattern=cls.ow.value, string=int_loc))

    @classmethod
    def is_msw(cls, int_loc: str) -> bool:
        """MSW locations start with 'OW76' or 'KW76' followed by 4 digits, eg. KW761234 or OW761234"""
        assert isinstance(int_loc, str)
        return bool(re.match(pattern=cls.msw.value, string=int_loc))

    @classmethod
    def find_type(cls, int_loc: str) -> "IntLocChoices":
        if cls.is_msw(int_loc=int_loc):
            return cls.msw
        elif cls.is_kw_hoofd(int_loc=int_loc):
            return cls.kw_hoofd
        elif cls.is_kw_sub(int_loc=int_loc):
            return cls.kw_sub
        elif cls.is_ow(int_loc=int_loc):
            return cls.ow


class IntParChoices(Enum):
    pass
