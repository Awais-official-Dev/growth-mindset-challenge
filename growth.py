import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title= "Data Sweeper", layout="wide")

# custom css
st.markdown(
        """
        <style>
        .stApp{
          background-color:black;
          color:white;
          }
          </style>
          """,
unsafe_allow_html=True
)

#title and  description
st.title("Data Sterling Integrator by Awais")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and creating the project for Quarter 3!")

#file uploader 
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_files:
    dataframes = {} 
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
           dataframes[file.name] = pd.read_csv(file)
        elif file_ext == ".xlsx":
           dataframes[file.name] = pd.read_excel(file)
        else:
           st.error(f"unsupported file type: {file_ext}")
           continue 
    #file data
    for file_name, df in dataframes.items():  # ✅ Har file ka dataframe loop me access karein
        st.write(f"Preview for {file_name}")
        st.dataframe(df.head())
    #data cleaning option
    st.subheader("Data Cleaning Option ")
   for file_name, df in dataframes.items():
       if st.checkbox(f"Clean data for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove duplicates from the file: {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates removed!")


            with col2:
                if st.button(f"fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been filled!")

        st.subheader("Select Columns to keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #data visualization 
        st.subheader("Data visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        #conversion option 
        st.subheader(" Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
         with pd.ExcelWriter(buffer, engine="openpyxl") as writer:  
                df.to_excel(writer, index=False)

                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name = file_name,
                mime= mime_type
            )

st.success(" All files processed successfully!")

