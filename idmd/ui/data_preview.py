# idmd/ui/data_preview.py
import streamlit as st

from .base import Component


class DataPreview(Component):
    """Component to display a preview of the dataset."""

    def render(self):
        if "df" in st.session_state:
            df = st.session_state.df
            st.dataframe(df.head())
