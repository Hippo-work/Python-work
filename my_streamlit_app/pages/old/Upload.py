import streamlit as st
import pandas as pd

st.title("📁 File Upload & Searchable Table")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Load file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Search & Filter")

    # Text search across all columns
    query = st.text_input("Search for a keyword")
    if query:
        df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    else:
        df_filtered = df

    st.dataframe(df_filtered, use_container_width=True)
