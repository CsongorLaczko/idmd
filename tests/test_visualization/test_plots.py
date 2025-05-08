import matplotlib.pyplot as plt
import pandas as pd
import pytest

from idmd.visualization.plots import PlotGenerator


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": [4, 5, 6],
        "category": ["A", "B", "A"]
    })


def test_generate_line_plot_returns_figure(sample_df):
    fig = PlotGenerator.generate_line_plot(sample_df, ["col1", "col2"])
    
    assert isinstance(fig, plt.Figure)

    ax = fig.axes[0]
    assert ax.get_title() == "Line Plot"
    assert ax.get_xlabel() == "Index"
    assert ax.get_ylabel() == "Values"
    # Optional: Check that both columns were plotted
    lines = ax.get_lines()
    assert len(lines) == 2


def test_generate_bar_plot_returns_figure(sample_df):
    fig = PlotGenerator.generate_bar_plot(sample_df, "category")
    
    assert isinstance(fig, plt.Figure)

    ax = fig.axes[0]
    assert ax.get_title() == "Bar Plot of category"
    assert ax.get_xlabel() == "Categories"
    assert ax.get_ylabel() == "Frequency"

    bars = [patch for patch in ax.patches if patch.get_height() > 0]
    assert len(bars) == 2  # Should have 2 categories: A and B
