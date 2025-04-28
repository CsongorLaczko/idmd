from typing import List, Optional

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
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

        col1, col2, col3 = st.columns([8, 1, 8])

        with col1:
            st.markdown("<h1 style='text-align: center;'>Description | Manipulation</h1>", unsafe_allow_html=True)
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

            # Reset to Default
            if st.button("Reset to Default Data"):
                if "original_df" in st.session_state:
                    st.session_state.df = st.session_state.original_df.copy()
                    st.success("Data has been reset to original upload.")
                else:
                    st.warning("No original data found to reset.")
    
            # Swap Two Columns
            st.markdown("<h3 style='text-align: center;'>Switch Two Columns</h3>", unsafe_allow_html=True)
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
            st.markdown("<h3 style='text-align: center;'>Drop a Column</h3>", unsafe_allow_html=True)
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
    
            # Replace Values
            st.markdown("<h3 style='text-align: center;'>Replace Values in Column</h3>", unsafe_allow_html=True)
    
            replace_col = st.selectbox("Select Column to Modify", df.columns)
            
            values_to_replace = st.selectbox(
                "Select Values to Replace",
                ["0", "np.nan", "outliers"]
            )
            
            replacement_method = st.selectbox(
                "Replace With",
                ["median", "min", "max", "random", "np.nan"]
            )
            
            if st.button("Apply Value Replacement"):
                if replace_col and values_to_replace and replacement_method:
                    col_data = df[replace_col]
                    if "0" in values_to_replace:
                        if "median" in replacement_method:
                            col_data = col_data.replace(0, col_data.median())
                        if "min" in replacement_method:
                            col_data = col_data.replace(0, col_data.min())
                        if "max" in replacement_method:
                            col_data = col_data.replace(0, col_data.max())
                        if "random" in replacement_method:
                            col_data = col_data.replace(0, col_data.sample(n=1).values[0])
                        if "np.nan" in replacement_method:
                            col_data = col_data.replace(0, pd.NA)
                    if "np.nan" in values_to_replace:
                        if "median" in replacement_method:
                            col_data = col_data.fillna(col_data.median())
                        if "min" in replacement_method:
                            col_data = col_data.fillna(col_data.min())
                        if "max" in replacement_method:
                            col_data = col_data.fillna(col_data.max())
                        if "random" in replacement_method:
                            col_data = col_data.fillna(col_data.dropna().sample(n=1).values[0])
                    if "outliers" in values_to_replace:
                        q1 = col_data.quantile(0.25)
                        q3 = col_data.quantile(0.75)
                        iqr = q3 - q1
                        lower = q1 - 1.5 * iqr
                        upper = q3 + 1.5 * iqr
                        outliers_mask = (col_data < lower) | (col_data > upper)
                        
                        if replacement_method == "median":
                            col_data[outliers_mask] = col_data.median()
                        elif replacement_method == "min":
                            col_data[outliers_mask] = col_data.min()
                        elif replacement_method == "max":
                            col_data[outliers_mask] = col_data.max()
                        elif replacement_method == "random":
                            col_data[outliers_mask] = col_data.drop(outliers_mask).sample(n=1).values[0]
                        elif replacement_method == "np.nan":
                            col_data[outliers_mask] = pd.NA
            
                    df[replace_col] = col_data
                    st.session_state.df = df.copy()
                    st.success(f"Values in '{replace_col}' replaced successfully.")
                else:
                    st.warning("Please select a column, values to replace, and replacement method.")
    
            # Download Data
            st.markdown("<h3 style='text-align: center;'>Download Processed Data</h3>", unsafe_allow_html=True)
            csv_data: str = df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data",
                data=csv_data,
                file_name="processed_data.csv",
                mime="text/csv",
            )
            
            # Download Report
            if st.button("Generate PDF Report"):
                pdf_buffer = create_pdf_report(df)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer,
                    file_name="data_report.pdf",
                    mime="application/pdf"
                )

        with col3:
            st.markdown("<h1 style='text-align: center;'>Data Visualization</h1>", unsafe_allow_html=True)

            # Column Overview DataFrame
            preview_data = pd.DataFrame({
                'Data Type': [df[col].dtype for col in df.columns],
                'Plottable': [pd.api.types.is_numeric_dtype(df[col]) for col in df.columns]
            }).T
            preview_data.columns = df.columns
            st.dataframe(preview_data)

            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            default_plot_cols = numeric_cols[:10]

            if "custom_plot_cols" not in st.session_state:
                st.session_state.custom_plot_cols = None
            if "custom_heatmap_cols" not in st.session_state:
                st.session_state.custom_heatmap_cols = None

            # Plot Columns
            st.markdown("<h3 style='text-align: center;'>Plot Selected Columns</h3>", unsafe_allow_html=True)
            plot_columns: List[str] = st.multiselect("Select Columns for Custom Plot", numeric_cols)

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
            st.markdown("<h3 style='text-align: center;'>Correlation Heatmap</h3>", unsafe_allow_html=True)
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

            # Histogram
            st.markdown("<h3 style='text-align: center;'>Histogram</h3>", unsafe_allow_html=True)
            default_hist_cols = numeric_cols[:10]
            custom_hist_cols: List[str] = st.multiselect("Select Columns for Custom Histogram", numeric_cols)

            if st.button("Generate Custom Histogram"):
                if custom_hist_cols:
                    fig, ax = plt.subplots()
                    df[custom_hist_cols].hist(ax=ax)
                    st.pyplot(fig)
                else:
                    st.warning("Please select at least one numeric column.")

            elif default_hist_cols:
                st.write("### Auto Histogram (First 10 Numeric Columns)")
                fig, ax = plt.subplots()
                df[default_hist_cols].hist(ax=ax)
                st.pyplot(fig)
            elif default_corr_cols:
                st.write("### Auto Heatmap (First 10 Numeric Columns)")
                fig, ax = plt.subplots()
                sns.heatmap(df[default_corr_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)


def create_pdf_report(df: pd.DataFrame) -> io.BytesIO:
    """
    Create a polished PDF report containing:
    - DataFrame preview
    - DataFrame statistics (rounded)
    - Line plot + correlation heatmap
    - Histograms in a compact grid
    """
    
    buffer = io.BytesIO()
    A4_inches = (8.27, 11.69)  # A4 size

    with PdfPages(buffer) as pdf:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        plot_cols = st.session_state.get('custom_plot_cols') or numeric_cols[:10]
        heatmap_cols = st.session_state.get('custom_heatmap_cols') or numeric_cols[:10]
        hist_cols = st.session_state.get('custom_hist_cols') or numeric_cols[:10]

        # --- Page 1: Preview + Description ---
        fig = plt.figure(figsize=A4_inches)
        gs = gridspec.GridSpec(4, 1, height_ratios=[1.5, 0.5, 2, 2])

        # DataFrame Preview
        ax1 = fig.add_subplot(gs[0])
        ax1.axis('off')
        # Add title manually inside the same axis
        ax1.set_title("Dataframe Preview")
        table1 = ax1.table(cellText=df.head().values, colLabels=df.columns, loc='center')
        table1.auto_set_font_size(False)
        table1.set_fontsize(8)
        table1.scale(1, 1.5)
        
        # DataFrame Describe
        desc = df.describe().round(3)
        ax2 = fig.add_subplot(gs[2])
        ax2.axis('off')
        ax2.set_title("Dataframe Statistics")
        table2 = ax2.table(cellText=desc.values, colLabels=desc.columns, rowLabels=desc.index, loc='center')
        table2.auto_set_font_size(False)
        table2.set_fontsize(6)
        table2.scale(1, 1.5)
        
        fig.tight_layout(pad=1.0)
        pdf.savefig(fig)
        plt.close(fig)

        # --- Page 2: Line Plot + Correlation Heatmap ---
        fig = plt.figure(figsize=A4_inches)
        gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])

        ax1 = fig.add_subplot(gs[0])
        if plot_cols:
            df[plot_cols].plot(ax=ax1)
            ax1.set_title('Line Plot of Selected Columns', fontsize=12, fontweight='bold')
        ax1.set_xlabel('')
        ax1.set_ylabel('')

        ax2 = fig.add_subplot(gs[1])
        if heatmap_cols:
            sns.heatmap(df[heatmap_cols].corr(), annot=True, cmap='coolwarm', ax=ax2, cbar=True)
            ax2.set_title('Correlation Heatmap', fontsize=12, fontweight='bold')

        fig.tight_layout(pad=0.5)
        pdf.savefig(fig)
        plt.close(fig)

        # --- Page 3: All Histograms in one Figure (grid layout) ---
        n_cols = 3 
        n_rows = (len(hist_cols) + n_cols - 1) // n_cols
        fig, axs = plt.subplots(n_rows, n_cols, figsize=A4_inches)

        axs = axs.flatten()

        for idx, col in enumerate(hist_cols):
            sns.histplot(df[col], kde=True, ax=axs[idx])
            axs[idx].set_title(f'Histogram of {col}', fontsize=10)
            axs[idx].set_xlabel('')
            axs[idx].set_ylabel('')

        # Hide any empty subplots
        for i in range(len(hist_cols), len(axs)):
            axs[i].axis('off')

        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

    buffer.seek(0)
    return buffer
