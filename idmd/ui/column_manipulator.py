# src/idmd/ui/column_manipulator.py
import streamlit as st

from ..ui.base import Component


class ColumnManipulator(Component):
    """Handles column operations and transformations"""

    def render(self):
        if "df" not in st.session_state:
            return

        self._render_column_swapper()
        self._render_column_dropper()
        self._render_column_selector()

    def _render_column_swapper(self):
        st.subheader("Swap Two Columns")
        col1, col2 = st.columns(2)

        with col1:
            col_a = st.selectbox("First Column", st.session_state.df.columns)
        with col2:
            col_b = st.selectbox("Second Column", st.session_state.df.columns)

        if st.button("Swap Columns") and col_a != col_b:
            self._swap_columns(col_a, col_b)

    def _swap_columns(self, col1, col2):
        cols = st.session_state.df.columns.tolist()
        i1, i2 = cols.index(col1), cols.index(col2)
        cols[i1], cols[i2] = cols[i2], cols[i1]
        st.session_state.df = st.session_state.df[cols]
        st.success(f"Swapped {col1} ↔ {col2}")

    def _render_column_dropper(self):
        st.subheader("Drop a Column")
        drop_col = st.selectbox("Select Column to Remove", st.session_state.df.columns)
        if st.button("Remove Column"):
            st.session_state.df = st.session_state.df.drop(columns=[drop_col])
            st.success(f"Removed column: {drop_col}")

    def _render_column_selector(self):
        st.subheader("Column Selection Filter")
        selected = st.multiselect(
            "Select Columns to Keep", st.session_state.df.columns, default=st.session_state.df.columns.tolist()
        )
        if st.button("Apply Selection Filter"):
            st.session_state.df = st.session_state.df[selected]
