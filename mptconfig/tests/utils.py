import pandas as pd  # noqa pandas comes with geopandas


def ensure_dataframes_equal(expected_df: pd.DataFrame, test_df: pd.DataFrame):
    # ensure ordered dfs (index and column)
    test_df = test_df.sort_index().sort_index(axis=1)
    expected_df = expected_df.sort_index().sort_index(axis=1)
    assert expected_df.equals(test_df)
