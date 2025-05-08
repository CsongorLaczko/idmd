from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from idmd.visualization.visualizer import DataVisualizer


@pytest.fixture
def sample_df():
    return pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": ["x", "y", "z"]})


@patch("idmd.visualization.visualizer.PlotGenerator")
def test_generate_line_plot_delegates(mock_plot_gen, sample_df):
    mock_fig = MagicMock()
    mock_plot_gen.generate_line_plot.return_value = mock_fig

    result = DataVisualizer.generate_line_plot(sample_df, ["a", "b"])
    mock_plot_gen.generate_line_plot.assert_called_once_with(sample_df, ["a", "b"])
    assert result == mock_fig


@patch("idmd.visualization.visualizer.PlotGenerator")
def test_generate_bar_plot_delegates(mock_plot_gen, sample_df):
    mock_fig = MagicMock()
    mock_plot_gen.generate_bar_plot.return_value = mock_fig

    result = DataVisualizer.generate_bar_plot(sample_df, "c")
    mock_plot_gen.generate_bar_plot.assert_called_once_with(sample_df, "c")
    assert result == mock_fig


@patch("idmd.visualization.visualizer.HeatmapGenerator")
def test_generate_correlation_heatmap_delegates(mock_heatmap_gen, sample_df):
    mock_fig = MagicMock()
    mock_heatmap_gen.generate_correlation_heatmap.return_value = mock_fig

    result = DataVisualizer.generate_correlation_heatmap(sample_df, ["a", "b"])
    mock_heatmap_gen.generate_correlation_heatmap.assert_called_once_with(sample_df, ["a", "b"])
    assert result == mock_fig


@patch("idmd.visualization.visualizer.HistogramGenerator")
def test_generate_histograms_delegates(mock_hist_gen, sample_df):
    mock_fig = MagicMock()
    mock_hist_gen.generate_histograms.return_value = mock_fig

    result = DataVisualizer.generate_histograms(sample_df, ["a", "b"])
    mock_hist_gen.generate_histograms.assert_called_once_with(sample_df, ["a", "b"])
    assert result == mock_fig


def test_generate_overview(sample_df):
    result = DataVisualizer.generate_overview(sample_df)

    assert isinstance(result, pd.DataFrame)
    assert "a" in result.columns
    assert "b" in result.columns
    assert "c" in result.columns
    assert result.loc["Data Type", "a"] == sample_df["a"].dtype
    assert result.loc["Plottable", "a"] is True
    assert result.loc["Plottable", "c"] is False
