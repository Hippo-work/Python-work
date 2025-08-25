import streamlit as st
import subprocess
import os
import sys

st.title("📂 Run Bash Script on Uploaded File")

uploaded_file = st.file_uploader("Choose a file")

#DSP Demod Parameters
sample_rate = st.text_input("Sample rate:")
center_freq = st.text_input("Center Frequency:")
# mod_type = st.text_input("Modulation type:")
# mod_rate = st.text_input("Modulation rate:")
# unique_word = st.text_input("UW:")


if uploaded_file is not None:
    # Streamlit stores uploaded files as temp files
    temp_path = uploaded_file.name
    st.success(f"File uploaded: {temp_path}")

    if st.button("Run Bash Script"):
        script_path = "C:/Users/rito0/OneDrive/Documents/Python/test_bash.sh"

        try:
            result = subprocess.run(
                ["C:/Program Files/Git/bin/bash.exe", script_path, temp_path],
                capture_output=True,
                text=True,
                check=True
            )
            st.code(result.stdout, language="bash")
            st.success("Processing complete!")
        except subprocess.CalledProcessError as e:
            st.error("Script failed:")
            st.code(e.stderr, language="bash")
        
            