import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Data Manipulator and Descriptor")

file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if file:
    # Initialize session state for the DataFrame
    if "df" not in st.session_state:
        st.session_state.df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)

    # Reference the stored DataFrame
    df = st.session_state.df
    
    st.write("## Data Preview")
    st.dataframe(df.head())
    
    # Data Description
    if st.checkbox("Show Summary Statistics"):
        st.write(df.describe())

    if st.checkbox("Show Column Info"):
        st.write(df.info())

    # Switch Two Columns
    if st.checkbox("Switch Two Columns"):
        st.write("## Swap Two Columns")
        col1, col2 = st.selectbox("Select First Column", df.columns, index=0), st.selectbox("Select Second Column", df.columns, index=1)
    
        if st.button("Swap Columns"):
            if col1 != col2:
                col_order = df.columns.tolist()
                idx1, idx2 = col_order.index(col1), col_order.index(col2)
                col_order[idx1], col_order[idx2] = col_order[idx2], col_order[idx1]
                st.session_state.df = df[col_order]
                st.success(f"Swapped '{col1}' and '{col2}'")
            else:
                st.warning("Please select two different columns.")

    # Drop a Column
    if st.checkbox("Drop Columns"):
        st.write("## Drop a Column")
        drop_col = st.selectbox("Select a Column to Drop", df.columns)
    
        if st.button("Drop Column"):
            df = df.drop(columns=[drop_col])
            st.success(f"Dropped column: {drop_col}")
            
        selected_columns = st.multiselect("Select Columns to Keep", df.columns, default=list(df.columns))
        st.session_state.df = df[selected_columns]

    # Visualization
    st.write("## Plot Selected Columns")
    plot_columns = st.multiselect("Select Columns to Plot", df.columns)

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
    st.download_button("Download Processed Data", df.to_csv(index=False), "processed_data.csv", "text/csv")
