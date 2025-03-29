from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


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
    st.title("Data Manipulator and Descriptor")

    file: Optional[st.runtime.uploaded_file_manager.UploadedFile] = st.file_uploader(
        "Upload a CSV or Excel file", type=["csv", "xlsx"]
    )

    if file is None and default_file:
        st.session_state.df = (
            pd.read_csv(default_file)
            if default_file.endswith(".csv")
            else pd.read_excel(default_file)
        )
    elif file:
        st.session_state.df = (
            pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        )

    if "df" in st.session_state:
        df: pd.DataFrame = st.session_state.df

        # Data preview
        st.write("## Data Preview")
        st.dataframe(df.head())

        # Data Description
        if st.checkbox("Show Summary Statistics"):
            st.write(df.describe())

        # Column information
        if st.checkbox("Show Column Info"):
            buffer = []
            df.info(buf=buffer)
            st.text("\n".join(buffer))

        # Switch Two Columns
        if st.checkbox("Switch Two Columns"):
            col1: str = st.selectbox("Select First Column", df.columns, index=0)
            col2: str = st.selectbox("Select Second Column", df.columns, index=1)

            if st.button("Swap Columns"):
                if col1 != col2:
                    col_order: List[str] = df.columns.tolist()
                    idx1, idx2 = col_order.index(col1), col_order.index(col2)
                    col_order[idx1], col_order[idx2] = col_order[idx2], col_order[idx1]
                    st.session_state.df = df[col_order]
                    st.success(f"Swapped '{col1}' and '{col2}'")
                else:
                    st.warning("Please select two different columns.")

        # Drop a Column
        if st.checkbox("Drop Columns"):
            st.write("## Drop a Column")
            drop_col: str = st.selectbox("Select a Column to Drop", df.columns)

            if st.button("Drop Column"):
                df.drop(columns=[drop_col], inplace=True)
                st.success(f"Dropped column: {drop_col}")

            selected_columns: List[str] = st.multiselect(
                "Select Columns to Keep", df.columns, default=list(df.columns)
            )
            st.session_state.df = df[selected_columns]

        # Visualization
        st.write("## Plot Selected Columns")
        plot_columns: List[str] = st.multiselect("Select Columns to Plot", df.columns)

        if st.button("Generate Plot"):
            if plot_columns:
                fig, ax = plt.subplots()
                df[plot_columns].plot(ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Please select at least one column to plot.")

        # Correlation Heatmap
        if st.checkbox("Show Correlation Heatmap"):
            fig, ax = plt.subplots()
            sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        # Export Data
        csv_data: str = df.to_csv(index=False)
        st.download_button(
            label="Download Processed Data",
            data=csv_data,
            file_name="processed_data.csv",
            mime="text/csv",
        )
