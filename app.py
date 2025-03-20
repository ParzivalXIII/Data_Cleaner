import streamlit as st
import pandas as pd
import io
from data_cleaner import clean_missing_values, remove_duplicates, convert_data_types
from data_visualizer import plot_bar_chart

st.set_page_config(page_title="XIII's Data Cleaning Tool", layout="wide")
st.title("🧹 Data Cleaning and Visualization Tool")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head())
    st.dataframe(df.tail())

    # Cleaning options
    st.sidebar.header("useful Cleaning Options")
    handle_missing = st.sidebar.checkbox("Handle Missing Values")
    remove_dups = st.sidebar.checkbox("Remove Duplicates")
    convert_types = st.sidebar.checkbox("Convert Data Types")

    # Apply cleaning
    cleaned_df = df.copy()

    if handle_missing:
        cleaned_df = clean_missing_values(cleaned_df)

    if remove_dups:
        cleaned_df = remove_duplicates(cleaned_df)

    if convert_types:
        cleaned_df = convert_data_types(cleaned_df)

    st.subheader("🧽 Cleaned Data Preview")
    st.dataframe(cleaned_df.head())
    st.dataframe(cleaned_df.tail())

    # Visualization options
    st.sidebar.header("Visualization")
    column_to_plot = st.sidebar.selectbox("Select column to visualize", cleaned_df.columns)
    sns_style = st.sidebar.selectbox("Seaborn Style", ["darkgrid", "whitegrid", "dark", "white", "ticks"], index=0)
    figsize = st.sidebar.slider("Figure Size (width, height)", 5, 20, (10, 6))
    bins = st.sidebar.slider("Bins (for numeric data)", 5, 50, 20)
    custom_title = st.sidebar.text_input("Custom Plot Title", "")

    if st.sidebar.button("Generate Plot"):
        st.subheader(f"📈 Visualization: {column_to_plot}")
        plot_bar_chart(cleaned_df, column_to_plot, sns_style=sns_style, figsize=figsize, 
                       title=custom_title if custom_title else None, bins=bins)

    # Download cleaned data
    buffer = io.StringIO()
    cleaned_df.to_csv(buffer, index=False)
    st.download_button(label="📥 Download Cleaned CSV (You're welcome 😊)",
                       data=buffer.getvalue(),
                       file_name="cleaned_data.csv",
                       mime="text/csv")
