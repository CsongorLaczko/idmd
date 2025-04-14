from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import io

def create_example(default_file: Optional[str] = None) -> None:
    """
    A Streamlit app for data manipulation, visualization, and exploration.

    This function creates an interactive web application where users can upload a CSV or Excel file,
    perform various operations on the dataset, and visualize the data. The app includes functionality for:

    - Previewing the uploaded dataset.
    - Displaying summary statistics and column information.
    - Swapping two columns in the dataset.
    - Dropping columns or selecting specific columns to keep.
    - Generating plots for selected columns.
    - Displaying a correlation heatmap of numerical features.
    - Exporting the processed dataset for download.

    Parameters:
    - default_file (Optional[str]): Path to a default CSV or Excel file to load initially. Defaults to None.

    Features:
        1. **File Upload**: Users can upload CSV or Excel files.
        2. **Data Preview**: Displays the first few rows of the dataset.
        3. **Summary Statistics**: Provides descriptive statistics for numerical columns.
        4. **Column Info**: Displays metadata about the dataset's columns (e.g., data types).
        5. **Column Manipulation**:
            - Swap two columns in the dataset.
            - Drop specific columns or select columns to keep.
        6. **Visualization**:
            - Plot selected columns using Matplotlib.
            - Generate a correlation heatmap using Seaborn.
        7. **Export Data**: Allows users to download the processed dataset as a CSV file.

    Usage:
        Run this function within a Streamlit app to interactively explore and manipulate datasets.

    Dependencies:
        - Streamlit (`streamlit`)
        - Pandas (`pandas`)
        - Seaborn (`seaborn`)
        - Matplotlib (`matplotlib`)

    """
    # Use Streamlit's wide layout mode
    st.set_page_config(layout="wide")
    
    st.title("Data Manipulator and Descriptor")

    file: Optional[st.runtime.uploaded_file_manager.UploadedFile] = st.file_uploader(
        "Upload a CSV or Excel file", type=["csv", "xlsx"]
    )

    if file and ("uploaded_file_name" not in st.session_state or st.session_state.uploaded_file_name != file.name):
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        st.session_state.original_df = df.copy()
        st.session_state.df = df.copy()
        st.session_state.uploaded_file_name = file.name

    if default_file and "original_df" not in st.session_state:
        df = pd.read_csv(default_file) if default_file.endswith(".csv") else pd.read_excel(default_file)
        st.session_state.original_df = df.copy()
        st.session_state.df = df.copy()

    if "df" in st.session_state:
        df = st.session_state.df

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown("<h1 style='text-align: center;'>Data Description</h1>", unsafe_allow_html=True)
            st.dataframe(df.head())

            # Basic Information
            if st.checkbox("Show Summary Statistics", value=True):
                st.write(df.describe())

            # Column Information
            if st.checkbox("Show Column Info"):
                buffer = io.StringIO()
                df.info(buf=buffer)
                info_str = buffer.getvalue()
                st.text(info_str)

        with col2:
            st.markdown("<h1 style='text-align: center;'>Data Manipulation</h1>", unsafe_allow_html=True)
    
            # Reset to Default
            if st.button("Reset to Default Data"):
                if "original_df" in st.session_state:
                    st.session_state.df = st.session_state.original_df.copy()
                    st.success("Data has been reset to original upload.")
                else:
                    st.warning("No original data found to reset.")

            # Swap Two Columns
            if st.checkbox("Switch Two Columns", value=True):
                st.write("## Switch Two Columns")
                col_1: str = st.selectbox("Select First Column", df.columns, index=0, key="switch1")
                col_2: str = st.selectbox("Select Second Column", df.columns, index=1, key="switch2")

                if st.button("Swap Columns"):
                    if col_1 != col_2:
                        col_order: List[str] = df.columns.tolist()
                        idx1, idx2 = col_order.index(col_1), col_order.index(col_2)
                        col_order[idx1], col_order[idx2] = col_order[idx2], col_order[idx1]
                        df = df[col_order]
                        st.session_state.df = df.copy()
                        st.success(f"Swapped '{col_1}' and '{col_2}'")
                    else:
                        st.warning("Please select two different columns.")

            # Drop Columns
            if st.checkbox("Drop Columns", value=True):
                st.write("## Drop a Column")
                drop_col: str = st.selectbox("Select a Column to Drop", df.columns)

                if st.button("Drop Column"):
                    df = df.drop(columns=[drop_col])
                    st.session_state.df = df.copy()
                    st.success(f"Dropped column: {drop_col}")

                selected_columns: List[str] = st.multiselect(
                    "Select Columns to Keep", df.columns, default=list(df.columns)
                )
                if st.button("Apply Column Selection"):
                    df = df[selected_columns]
                    st.session_state.df = df.copy()
                    st.success("Selected columns updated.")

            # Download Data
            st.write("## Download Processed Data")
            csv_data: str = df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data",
                data=csv_data,
                file_name="processed_data.csv",
                mime="text/csv",
            )

        with col3:
            st.markdown("<h1 style='text-align: center;'>Data Visualization</h1>", unsafe_allow_html=True)

            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            default_plot_cols = numeric_cols[:10]

            if "custom_plot_cols" not in st.session_state:
                st.session_state.custom_plot_cols = None
            if "custom_heatmap_cols" not in st.session_state:
                st.session_state.custom_heatmap_cols = None

            # Plot Columns
            st.write("## Plot Selected Columns")
            plot_columns: List[str] = st.multiselect("Select Columns for Custom Plot", df.columns)

            if st.button("Generate Custom Plot"):
                if plot_columns:
                    st.session_state.custom_plot_cols = plot_columns
                else:
                    st.warning("Please select at least one column to plot.")

            if st.session_state.custom_plot_cols:
                fig, ax = plt.subplots()
                df[st.session_state.custom_plot_cols].plot(ax=ax)
                st.pyplot(fig)
            elif default_plot_cols:
                st.write("### Auto Plot (First 10 Numeric Columns)")
                fig, ax = plt.subplots()
                df[default_plot_cols].plot(ax=ax)
                st.pyplot(fig)

            # Correlation Heatmap
            st.write("## Correlation Heatmap")
            default_corr_cols = numeric_cols[:10]
            custom_corr_cols: List[str] = st.multiselect("Select Columns for Custom Heatmap", numeric_cols)

            if st.button("Generate Custom Heatmap"):
                if custom_corr_cols:
                    st.session_state.custom_heatmap_cols = custom_corr_cols
                else:
                    st.warning("Please select at least one numeric column.")

            if st.session_state.custom_heatmap_cols:
                fig, ax = plt.subplots()
                sns.heatmap(df[st.session_state.custom_heatmap_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)
            elif default_corr_cols:
                st.write("### Auto Heatmap (First 10 Numeric Columns)")
                fig, ax = plt.subplots()
                sns.heatmap(df[default_corr_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)
