import streamlit as st
import pandas as pd
import io
from data_cleaner import clean_missing_values, remove_duplicates, convert_data_types
from data_visualizer import plot_bar_chart, plot_pie_chart, plot_histogram

st.set_page_config(page_title="XIII's Data Cleaning Tool", layout="wide")
st.title("🧹 Data Cleaning and Visualization Tool(XIII)")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Original Data Preview")
    st.dataframe(df.head())
    st.dataframe(df.tail())

    # Cleaning options
    st.sidebar.header("Useful Cleaning Options")
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
    
    is_numeric = pd.api.types.is_numeric_dtype(cleaned_df[column_to_plot])
    unique_vals = cleaned_df[column_to_plot].nunique()
    if is_numeric:
        chart_type = st.sidebar.selectbox('chart type', ['Histogram'])
    else:
        if unique_vals <= 10:
            chart_type  = st.sidebar.selectbox('Chart Type', ['Bar Chart', 'Pie Chart'])
        else:
            chart_type = st.sidebar.selectbox('Chart Type', ['Bar Chart'])

if st.sidebar.button("Generate Plot"):
    st.subheader(f"📈 Visualization: {column_to_plot}")

    # ✅ Generate the plot based on selection
    if chart_type == 'Histogram':
        fig = plot_histogram(
            cleaned_df,
            column_name=column_to_plot,
            sns_style=sns_style,
            figsize=figsize,
            title=custom_title if custom_title else None,
            bins=bins
        )
    elif chart_type == 'Pie Chart':
        fig = plot_pie_chart(
            cleaned_df,
            column_name=column_to_plot,
            title=custom_title if custom_title else None
        )
    else:
        fig = plot_bar_chart(
            cleaned_df,
            column_name=column_to_plot,
            sns_style=sns_style,
            figsize=figsize,
            title=custom_title if custom_title else None,
            bins=bins
        )


    # ✅ Display the plot
    st.pyplot(fig)

    # ✅ Save the plot to an in-memory buffer for download
    plot_buffer = io.BytesIO()
    fig.savefig(plot_buffer, format='png', dpi=300, bbox_inches='tight')
    plot_buffer.seek(0)

    # ✅ Download button for the plot
    st.download_button(
        label="📥 Download Plot as PNG",
        data=plot_buffer,
        file_name=f"{column_to_plot}_plot.png",
        mime="image/png"
    )


    # Download cleaned data
    buffer = io.StringIO()
    cleaned_df.to_csv(buffer, index=False)
    st.download_button(label="📥 Download Cleaned CSV (You're welcome 😊)",
                       data=buffer.getvalue(),
                       file_name="cleaned_data.csv",
                       mime="text/csv")
