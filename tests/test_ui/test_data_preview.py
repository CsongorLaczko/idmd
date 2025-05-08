from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from idmd.ui.data_preview import DataPreview


@pytest.fixture
def sample_df():
    return pd.DataFrame({"a": [1, 2], "b": [3, 4]})


@patch("idmd.ui.data_preview.st")
def test_render_shows_preview(mock_st, sample_df):
    session_state = MagicMock()
    session_state.__contains__.side_effect = lambda key: key in ["df", "original_df"]
    session_state.df = sample_df
    session_state.original_df = sample_df.copy()
    session_state._refresh_preview = False
    mock_st.session_state = session_state

    mock_st.columns.return_value = [MagicMock(), MagicMock(), MagicMock()]
    mock_st.button.side_effect = [False, False]

    comp = DataPreview()
    comp.render()

    mock_st.header.assert_called_once_with("Dataset Preview")
    args, _ = mock_st.dataframe.call_args
    pd.testing.assert_frame_equal(args[0], sample_df.head())
    assert session_state._refresh_preview is False


@patch("idmd.ui.data_preview.st")
def test_refresh_preview_button(mock_st, sample_df):
    session_state = MagicMock()
    session_state.__contains__.side_effect = lambda key: key == "df"
    session_state.df = sample_df
    session_state._refresh_preview = False
    mock_st.session_state = session_state

    col1, col2, _ = MagicMock(), MagicMock(), MagicMock()
    mock_st.columns.return_value = [col1, col2, _]
    col1.button.return_value = True
    col2.button.return_value = False

    comp = DataPreview()
    comp.render()

    assert session_state._refresh_preview is True


@patch("idmd.ui.data_preview.st")
def test_reset_to_default_data_success(mock_st, sample_df):
    session_state = MagicMock()
    session_state.__contains__.side_effect = lambda key: key in ["df", "original_df"]
    session_state.df = sample_df.copy()
    session_state.original_df = sample_df
    session_state._refresh_preview = False
    mock_st.session_state = session_state

    col1, col2, _ = MagicMock(), MagicMock(), MagicMock()
    mock_st.columns.return_value = [col1, col2, _]
    col1.button.return_value = False
    col2.button.return_value = True

    comp = DataPreview()
    comp.render()

    pd.testing.assert_frame_equal(session_state.df, sample_df)
    assert session_state._refresh_preview is True
    mock_st.success.assert_called_once_with("Data has been reset to original upload.")


@patch("idmd.ui.data_preview.st")
def test_reset_to_default_data_missing(mock_st, sample_df):
    session_state = MagicMock()
    session_state.__contains__.side_effect = lambda key: key == "df"
    session_state.df = sample_df.copy()
    session_state._refresh_preview = False
    mock_st.session_state = session_state

    col1, col2, _ = MagicMock(), MagicMock(), MagicMock()
    mock_st.columns.return_value = [col1, col2, _]
    col1.button.return_value = False
    col2.button.return_value = True

    comp = DataPreview()
    comp.render()

    mock_st.warning.assert_called_once_with("No original data found to reset.")
