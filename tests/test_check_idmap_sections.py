# from mptconfig.checker import MptConfigChecker
# from pandas._testing import assert_frame_equal
#
# import pandas as pd
# import pytest
# from unittest import mock
# # from the_module import Test1, OneMissingException
# from mptconfig.constants import PathConstants
#
# @pytest.fixture
# def patched_my_dict(monkeypatch):
#     patched = {'one': 1, 'two': 2, 'three': 3}
#
#     monkeypatch.setattr("constants.MY_DICT", patched)
#     return patched
#
# def test_verify_test1_exception(patched_my_dict):
#     patched_my_dict.pop('one') # comment this out and test will not pass
#     with pytest.raises(OneMissingException):
#         Test1()
#
#
#
# def test_check_idmap_sections():
#     meetpunt_config = MptConfigChecker()
#     sheet_name, result_df = meetpunt_config.check_idmap_sections()
#     assert isinstance(sheet_name, str) and isinstance(result_df, pd.DataFrame)
#     assert sheet_name == "idmap section error"
