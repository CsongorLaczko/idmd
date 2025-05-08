import pandas as pd

from idmd.manipulation.replace import ReplaceLogic


def test_replace_zeros_with_median():
    """Test replacing zeros with the column median."""
    df = pd.DataFrame({"A": [0, 2, 3, 0, 5]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="0", replacement_method="median")

    assert updated_df["A"].tolist() == [3, 2, 3, 3, 5], "Zeros should be replaced with the median (3)."


def test_replace_nan_with_min():
    """Test replacing NaN values with the column minimum."""
    df = pd.DataFrame({"A": [1, None, 3, None, 5]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="np.nan", replacement_method="min")

    assert updated_df["A"].tolist() == [1, 1, 3, 1, 5], "NaN values should be replaced with the minimum (1)."


def test_replace_outliers_with_max():
    """Test replacing outliers with the column maximum."""
    df = pd.DataFrame({"A": [1, 2, 100, 3, 4]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="outliers", replacement_method="max")

    assert updated_df["A"].tolist() == [1, 2, 4, 3, 4], "Outliers should be replaced with the maximum (4)."


def test_replace_zeros_with_random():
    """Test replacing zeros with a random value from the column."""
    df = pd.DataFrame({"A": [0, 2, 3, 0, 5]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="0", replacement_method="random")

    assert 0 not in updated_df["A"].tolist(), "Zeros should be replaced with random values from the column."
    assert len(updated_df["A"].unique()) <= len(df["A"].unique()), "Random replacement should not introduce new values."


def test_replace_nan_with_nan():
    """Test replacing NaN values with NaN explicitly."""
    df = pd.DataFrame({"A": [1, None, 3, None, 5]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="np.nan", replacement_method="np.nan")

    assert updated_df["A"].isna().sum() == 2, "NaN values should remain as NaN."


def test_replace_outliers_with_nan():
    """Test replacing outliers with NaN."""
    df = pd.DataFrame({"A": [1, 2, 100, 3, 4]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="outliers", replacement_method="np.nan")

    assert updated_df["A"].isna().sum() == 1, "Outliers should be replaced with NaN."
    expected_result = pd.Series([1, 2, None, 3, 4], name="A", dtype="float")
    pd.testing.assert_series_equal(updated_df["A"], expected_result, check_dtype=False, obj="Outliers Replacement")


def test_replace_all_with_max():
    """Test replacing all missing values with the column maximum."""
    df = pd.DataFrame({"A": [None, 2, 3, None, 5]})
    updated_df = ReplaceLogic.replace_values(df, column="A", values_to_replace="all", replacement_method="max")

    assert updated_df["A"].tolist() == [5, 2, 3, 5, 5], "All missing values should be replaced with the maximum (5)."