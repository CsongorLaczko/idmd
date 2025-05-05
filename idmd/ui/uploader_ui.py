"""Module for file uploader component."""
import time

import pandas as pd
import streamlit as st

from ..data.uploader import FileUploader
from ..data.generator import DatasetGenerator
from .base import Component


class FileUploaderGeneratorUI(Component):
    """Provides UI for file uploading and generation."""

    def __init__(self, position: int = 0, file_types=None, default_file=None) -> None:
        """
        Initializes the FileUploaderUI component with a specific position, file types, and a default file.

        Args:
            position (int): The column position of the component. Defaults to 0.
            file_types (list, optional): List of allowed file types for upload. Defaults to ["csv", "xlsx"].
            default_file (str, optional): Path to a default file to load if no file is uploaded. Defaults to None.
        """
        super().__init__(position)
        self.uploader = FileUploader(file_types=file_types, default_file=default_file)

    def render(self) -> None:
        """
        Renders the file uploader and generator in the Streamlit interface.

        Handles file uploads, data generation and initializes the dataset in the session state.
        """
        st.header("Data Initialization")
        uploaded_file = st.file_uploader(
            "Upload a CSV or Excel file", type=self.uploader.file_types, key="file_uploader"
        )

        if uploaded_file and self.uploader.is_new_file(uploaded_file, st.session_state):
            self.uploader.process_upload(uploaded_file, st.session_state)

        if self.uploader.default_file and not st.session_state.get("df"):
            try:
                self.uploader.load_default_file(st.session_state)
            except ValueError as e:
                st.error(str(e))

        st.markdown("-- OR --")

        selected_distribution = st.selectbox("Dataset Generation", options=["normal", "uniform", "random"])

        sample_count = st.number_input("Sample Size", min_value=1, step=1)
        column_count = st.number_input("Column Size", min_value=1, step=1)

        size = (sample_count, column_count)

        params: dict[str, int|float] = {}

        if selected_distribution == "normal":
            params["normal_mean"] = st.number_input("Mean")
            params["normal_sd"] = st.number_input("Standard Deviation", min_value=0)

        elif selected_distribution == "uniform":
            params["uni_lb"] = st.number_input("Lower Bound")
            params["uni_ub"] = st.number_input("Upper Bound")

        elif selected_distribution == "random":
            params["rnd_lb"] = st.number_input("Lower Bound", step=1)
            params["rnd_ub"] = st.number_input("Upper Bound", step=1)

        data: pd.DataFrame

        if st.button("Generate Dataset"):
            if selected_distribution == "normal":
                data = DatasetGenerator.generate_normal_distribution(size, params["normal_mean"], params["normal_sd"])
            elif selected_distribution == "uniform":
                data = DatasetGenerator.generate_uniform_distribution(size, params["uni_lb"], params["uni_ub"])
            elif selected_distribution == "random":
                data = DatasetGenerator.generate_random_integers(size, params["rnd_lb"], params["rnd_ub"])

            st.session_state["original_df"] = data.copy()
            st.session_state["df"] = data.copy()
            st.session_state["uploaded_file_name"] = f"{selected_distribution}_{time.time_ns()}.csv"