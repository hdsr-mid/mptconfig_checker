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
    ow = "OW......$"
    kw_hoofd = "KW.....0$"
    kw_sub = "KW.....[1-9]$"

    @classmethod
    def is_ow(cls, int_loc: str) -> bool:
        """OW locations start with 'OW' followed by 6 digits, eg. OW123456"""
        assert isinstance(int_loc, str)
        return bool(re.match(pattern=cls.ow.value, string=int_loc))

    @classmethod
    def is_kw_hoofd(cls, int_loc: str) -> bool:
        """Hoofdlocations start with 'KW' followed by 6 digits with the last being 0, eg. KW123450"""
        assert isinstance(int_loc, str)
        return bool(re.match(pattern=cls.kw_hoofd.value, string=int_loc))

    @classmethod
    def is_kw_sub(cls, int_loc: str) -> bool:
        """Sublocations start with 'KW' followed by 6 digits with the last not being 0, eg. KW123451"""
        assert isinstance(int_loc, str)
        return bool(re.match(pattern=cls.kw_sub.value, string=int_loc))

    @classmethod
    def is_kw(cls, int_loc: str) -> bool:
        return True if cls.is_kw_sub(int_loc) or cls.is_kw_hoofd(int_loc) else False

    @classmethod
    def is_kw_or_ow(cls, int_loc: str) -> bool:
        return True if cls.is_kw(int_loc) or cls.is_ow(int_loc) else False

    @classmethod
    def find_type(cls, int_loc: str) -> "IntLocChoices":
        if cls.is_ow(int_loc=int_loc):
            return cls.ow
        elif cls.is_kw_hoofd(int_loc=int_loc):
            return cls.kw_hoofd
        elif cls.is_kw_sub(int_loc=int_loc):
            return cls.kw_sub


class IntParChoices(Enum):
    pass
