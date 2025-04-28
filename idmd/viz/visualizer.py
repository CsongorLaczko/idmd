# src/idmd/viz/visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from ..ui.base import Component


class DataVisualizer(Component):
    """Handles data visualization components"""

    @property
    def position(self):
        return "right"

    def render(self):
        if "df" not in st.session_state:
            return

        self._render_auto_plots()
        self._render_custom_visualizations()

    def _render_auto_plots(self):
        st.subheader("Automated Visual Analysis")
        self._plot_initial_columns()
        self._show_correlation_heatmap()

    def _plot_initial_columns(self):
        numeric_cols = st.session_state.df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            fig, ax = plt.subplots()
            st.session_state.df[numeric_cols[:10]].plot(ax=ax)
            st.pyplot(fig)

    def _show_correlation_heatmap(self):
        numeric_cols = st.session_state.df.select_dtypes(include="number").columns
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(st.session_state.df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

    def _render_custom_visualizations(self):
        st.subheader("Custom Visualization Builder")
        self._create_custom_plot()
        self._create_histogram()

    def _create_custom_plot(self):
        selected = st.multiselect("Select Plot Columns", st.session_state.df.select_dtypes(include="number").columns)
        if selected and st.button("Generate Custom Plot"):
            fig, ax = plt.subplots()
            st.session_state.df[selected].plot(ax=ax)
            st.pyplot(fig)

    def _create_histogram(self):
        selected = st.multiselect(
            "Select Histogram Columns", st.session_state.df.select_dtypes(include="number").columns
        )
        if selected and st.button("Generate Histograms"):
            fig, ax = plt.subplots()
            st.session_state.df[selected].hist(ax=ax)
            st.pyplot(fig)
