import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="🧹 Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
      background-color: black;
      color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📊 Data Sterling Integrator by Awais 🚀")
st.write("🔄 Transform your files between CSV and Excel formats with built-in data cleaning! 🎯")

# File uploader
uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    dataframes = {}

    # Read uploaded files
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            dataframes[file.name] = pd.read_csv(file)
        elif file_ext == ".xlsx":
            dataframes[file.name] = pd.read_excel(file, engine="openpyxl")
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

    # File data preview
    for file_name, df in dataframes.items():
        st.write(f"🔍 **Preview for {file_name}**")
        st.dataframe(df.head())

    # Data cleaning options
    st.subheader("🧼 Data Cleaning Options")
    for file_name, df in dataframes.items():
        if st.checkbox(f"🛠️ Clean data for {file_name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove duplicates from {file_name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🛠️ Fill missing values for {file_name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")

            st.subheader("🎯 Select Columns to Keep")
            columns = st.multiselect(f"📌 Choose columns for {file_name}", df.columns, default=df.columns)
            df = df[columns]

            # Data visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show visualization for {file_name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

            # Conversion options
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"📂 Convert {file_name} to:", ["CSV", "Excel"], key=file_name)

            if st.button(f"⬇️ Convert & Download {file_name}"):
                buffer = BytesIO()

                if conversion_type == "CSV":
                    buffer.write(df.to_csv(index=False).encode())
                    file_download_name = file_name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False)
                    buffer.seek(0)
                    file_download_name = file_name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                st.download_button(
                    label=f"📥 Download {file_name} as {conversion_type}",
                    data=buffer,
                    file_name=file_download_name,
                    mime=mime_type
                )

st.success("🎉 All files processed successfully! 🚀")
