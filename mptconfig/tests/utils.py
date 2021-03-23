import pandas as pd  # noqa pandas comes with geopandas


def equal_dataframes(expected_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
    """A helper function to ensure that a dataframe check result equals an expected dataframe. """
    # ensure ordered dfs (index and column)
    test_df = test_df.sort_index().sort_index(axis=1)
    expected_df = expected_df.sort_index().sort_index(axis=1)
    return expected_df.equals(test_df)
