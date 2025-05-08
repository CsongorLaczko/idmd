import pandas as pd
from idmd.data.exporter import DataExporter


def test_export_to_csv_creates_valid_csv():
    """Test that the exporter creates a valid CSV string from a DataFrame."""
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    csv_data = DataExporter.export_to_csv(df)

    assert "col1,col2" in csv_data, "The CSV data should contain the column headers."
    assert "1,4" in csv_data, "The CSV data should contain the first row of data."
    assert "2,5" in csv_data, "The CSV data should contain the second row of data."
    assert "3,6" in csv_data, "The CSV data should contain the third row of data."


def test_validate_data_with_existing_df():
    """Test that the validation function returns True when a DataFrame exists in session state."""
    session_state = {"df": pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})}
    assert DataExporter.validate_data(session_state), "The dataset should exist in the session state."
