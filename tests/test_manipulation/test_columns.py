import pandas as pd
from idmd.manipulation.columns import ColumnManipulatorLogic


def test_swap_columns():
    """Test swapping two columns in a DataFrame."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    swapped_df = ColumnManipulatorLogic.swap_columns(df, "A", "B")

    assert list(swapped_df.columns) == ["B", "A"], "The columns should be swapped."
    assert swapped_df["A"].tolist() == [3, 4], "The values in column A should match the original column B."
    assert swapped_df["B"].tolist() == [1, 2], "The values in column B should match the original column A."


def test_drop_column():
    """Test dropping a column from a DataFrame."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    modified_df = ColumnManipulatorLogic.drop_column(df, "A")

    assert "A" not in modified_df.columns, "The column 'A' should be dropped."
    assert list(modified_df.columns) == ["B"], "Only column 'B' should remain."


def test_select_columns():
    """Test selecting specific columns from a DataFrame."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    selected_df = ColumnManipulatorLogic.select_columns(df, ["A", "C"])

    assert list(selected_df.columns) == ["A", "C"], "Only columns 'A' and 'C' should be selected."
    assert selected_df.shape == (2, 2), "The resulting DataFrame should have 2 rows and 2 columns."
