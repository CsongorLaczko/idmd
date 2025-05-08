import matplotlib.pyplot as plt
import pandas as pd

from idmd.visualization.histograms import HistogramGenerator


def test_generate_histograms_valid_columns():
    """Test generating histograms with valid columns."""
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],
        "C": [2, 3, 4, 5, 6]
    })

    fig = HistogramGenerator.generate_histograms(df, columns=["A", "B", "C"])

    assert isinstance(fig, plt.Figure), "The output should be a matplotlib Figure."
    assert len(fig.axes) == 3, "The figure should contain three subplots (one for each column)."
    assert fig.axes[0].get_title() == "Histogram of A", "The first subplot title should be 'Histogram of A'."
    assert fig.axes[1].get_title() == "Histogram of B", "The second subplot title should be 'Histogram of B'."
    assert fig.axes[2].get_title() == "Histogram of C", "The third subplot title should be 'Histogram of C'."


def test_generate_histograms_missing_column():
    """Test generating histograms with a missing column."""
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1]
    })

    try:
        HistogramGenerator.generate_histograms(df, columns=["A", "B", "C"])
    except KeyError as e:
        assert "C" in str(e), "The error message should indicate the missing column."


def test_generate_histograms_empty_dataframe():
    """Test generating histograms with an empty DataFrame."""
    df = pd.DataFrame()

    try:
        HistogramGenerator.generate_histograms(df, columns=[])
    except ValueError as e:
        assert "Number of rows must be a positive integer, not 0" in str(e), "The error message should indicate that there is no data."


def test_generate_histograms_single_column():
    """Test generating a histogram with a single column."""
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5]
    })

    fig = HistogramGenerator.generate_histograms(df, columns=["A"])

    assert isinstance(fig, plt.Figure), "The output should be a matplotlib Figure."
    assert len(fig.axes) >= 1, "The figure should contain at least one subplot."
    assert fig.axes[0].get_title() == "Histogram of A", "The subplot title should be 'Histogram of A'."
    for ax in fig.axes[1:]:
        assert not ax.has_data(), "Extra axes should be empty."


def test_generate_histograms_extra_empty_subplots():
    """Test that extra subplots are empty when the number of columns is less than the grid size."""
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1]
    })

    fig = HistogramGenerator.generate_histograms(df, columns=["A", "B"])

    assert isinstance(fig, plt.Figure), "The output should be a matplotlib Figure."
    assert len(fig.axes) == 3, "The figure should contain three subplots (grid size is 3)."
    assert not fig.axes[2].has_data(), "The third subplot should be empty as there are only two columns."