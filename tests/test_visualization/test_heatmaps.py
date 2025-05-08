import matplotlib.pyplot as plt
import pandas as pd
from idmd.visualization.heatmaps import HeatmapGenerator


def test_generate_correlation_heatmap_valid_columns():
    """Test generating a correlation heatmap with valid columns."""
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1], "C": [2, 3, 4, 5, 6]})

    fig = HeatmapGenerator.generate_correlation_heatmap(df, columns=["A", "B", "C"])

    assert isinstance(fig, plt.Figure), "The output should be a matplotlib Figure."
    assert len(fig.axes) > 0, "The figure should contain at least one axis."
    assert fig.axes[0].get_title() == "Correlation Heatmap", "The heatmap title should be 'Correlation Heatmap'."


def test_generate_correlation_heatmap_missing_column():
    """Test generating a correlation heatmap with a missing column."""
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [5, 4, 3, 2, 1]})

    try:
        HeatmapGenerator.generate_correlation_heatmap(df, columns=["A", "B", "C"])
    except KeyError as e:
        assert "C" in str(e), "The error message should indicate the missing column."


def test_generate_correlation_heatmap_empty_dataframe():
    """Test generating a correlation heatmap with an empty DataFrame."""
    df = pd.DataFrame()

    try:
        HeatmapGenerator.generate_correlation_heatmap(df, columns=[])
    except ValueError as e:
        assert "zero-size array" in str(e), "The error message should indicate that there is no data."


def test_generate_correlation_heatmap_single_column():
    """Test generating a correlation heatmap with a single column."""
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})

    fig = HeatmapGenerator.generate_correlation_heatmap(df, columns=["A"])

    assert isinstance(fig, plt.Figure), "The output should be a matplotlib Figure."
    assert len(fig.axes) > 0, "The figure should contain at least one axis."
    assert fig.axes[0].get_title() == "Correlation Heatmap", "The heatmap title should be 'Correlation Heatmap'."
