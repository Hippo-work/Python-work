from time import sleep
import streamlit as st
import subprocess
import os
import sys
import tempfile
import json
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

st.title("📂 Run Bash Script on Uploaded File")

uploaded_file = st.file_uploader("Choose a file")

#DSP Demod Parameters
# sample_rate = st.text_input("Sample rate:")
# center_freq = st.text_input("Center Frequency:")
# mod_type = st.text_input("Modulation type:")
# mod_rate = st.text_input("Modulation rate:")
# unique_word = st.text_input("UW:")

if uploaded_file is not None:
    # Streamlit stores uploaded files as temp files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tmp:
        tmp.write(uploaded_file.read())
        raw_temp_path = tmp.name
        temp_path = str(Path(raw_temp_path).as_posix())
        st.write(f"temp path", temp_path)
    st.success(f"File uploaded: {uploaded_file.name}")

    #Load scripts
    with open("scripts/scripts.json") as f:
        available_scripts = json.load(f)
        full_script = set(available_scripts)
    #select script to use
    st.session_state.picked_script = st.selectbox("Choose Script to Run:", available_scripts)


    st.session_state.arg_entry = available_scripts[st.session_state.picked_script]
    st.write(st.session_state.arg_entry["arguments"])
    args = ""
    for arg_key, arg_value in st.session_state.arg_entry["arguments"].items():
        st.write(arg_key, arg_value)
        args += (arg_value + " ") 
    
    if st.button("Run Bash Script"): # and arg1 and arg2:
        script_entry = available_scripts[st.session_state.picked_script]
        raw_path = script_entry["module"]  # e.g. "scripts/test.sh"
        script_path = str(Path(raw_path).as_posix())
        st.write(script_path)
        
        # arg1 = arg_entry["arguments"]["stop"]
        

        temp_proc_path = "downloads/tmp.bit"
        output_path = "downloads/out.bit"

        try:
            result = subprocess.run(
                ["C:/Program Files/Git/bin/bash.exe", 
                script_path,
                temp_path, 
                str(args),
                ],
                capture_output=True,
                text=True,
                check=True
            )
            st.code(result.stdout, language="bash")
            st.success("Processing complete!")
        except subprocess.CalledProcessError as e:
            st.error("Script failed:")
            st.code(e.stderr, language="bash")
    os.remove(temp_path)
            