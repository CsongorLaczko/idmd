# idmd/data/loader.py
import pandas as pd
import streamlit as st

from ..ui.base import Component


class FileUploader(Component):
    """Handles file upload and data initialization"""

    def __init__(self, file_types=None, default_file=None):
        self.file_types = file_types or ["csv", "xlsx"]
        self.default_file = default_file

    def render(self):
        uploaded_file = st.file_uploader("Upload data file", type=self.file_types, key="file_uploader")

        if uploaded_file and self._is_new_file(uploaded_file):
            self._process_upload(uploaded_file)

        if self.default_file and not st.session_state.get("df"):
            self._load_default_file()

    def _is_new_file(self, file):
        return st.session_state.get("uploaded_file_name") != file.name

    def _process_upload(self, file):
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        st.session_state.original_df = df.copy()
        st.session_state.df = df.copy()
        st.session_state.uploaded_file_name = file.name

    def _load_default_file(self):
        loader = pd.read_csv if self.default_file.endswith(".csv") else pd.read_excel
        df = loader(self.default_file)
        st.session_state.original_df = df.copy()
        st.session_state.df = df.copy()
