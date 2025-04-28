# src/idmd/data/exporter.py
import streamlit as st

from ..ui.base import Component


class DataExporter(Component):
    """Handles data export functionality"""

    def render(self):
        if "df" not in st.session_state:
            return

        st.subheader("Data Export")
        self._configure_export()

    def _configure_export(self):
        export_df = st.session_state.df
        csv_data = export_df.to_csv(index=False)

        st.download_button(
            label="Download Processed Data",
            data=csv_data,
            file_name="processed_data.csv",
            mime="text/csv",
            key="export_button",
        )
