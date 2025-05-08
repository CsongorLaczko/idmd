import pytest
from idmd.data.uploader import FileUploader


def test_is_new_file():
    """Test that the uploader correctly identifies a new file."""
    uploader = FileUploader()
    session_state = {"uploaded_file_name": "old_file.csv"}
    new_file = type("File", (object,), {"name": "new_file.csv"})()

    assert uploader.is_new_file(new_file, session_state), "The new file should be recognized as new."


def test_process_upload_valid_csv(tmp_path):
    """Test that the uploader correctly processes a valid CSV file."""
    uploader = FileUploader()
    session_state = {}
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")

    with open(csv_file, "r") as file:
        uploader.process_upload(file, session_state)

    assert "df" in session_state, "The session state should contain the uploaded DataFrame."
    assert session_state["df"].shape == (2, 2), "The DataFrame should have 2 rows and 2 columns."
    assert list(session_state["df"].columns) == ["col1", "col2"], "The DataFrame should have the correct columns."


def test_process_upload_handles_invalid_file(tmp_path):
    """Test that the uploader gracefully handles invalid file formats."""
    uploader = FileUploader()
    session_state = {}
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("This is not a CSV file.")

    with pytest.raises(ValueError, match="format cannot be determined"):
        with open(invalid_file, "r") as file:
            uploader.process_upload(file, session_state)


def test_load_default_file_valid_csv(tmp_path):
    """Test loading a valid default CSV file."""
    csv_file = tmp_path / "default.csv"
    csv_file.write_text("col1,col2\n1,2\n3,4")
    uploader = FileUploader(default_file=str(csv_file))
    session_state = {}

    uploader.load_default_file(session_state)

    assert "df" in session_state, "The session state should contain the loaded DataFrame."
    assert session_state["df"].shape == (2, 2), "The DataFrame should have 2 rows and 2 columns."
    assert list(session_state["df"].columns) == ["col1", "col2"], "The DataFrame should have the correct columns."


def test_default_file_not_specified():
    """Test that an error is raised if no default file is specified."""
    uploader = FileUploader()
    session_state = {}

    with pytest.raises(ValueError, match="No default file specified."):
        uploader.load_default_file(session_state)
