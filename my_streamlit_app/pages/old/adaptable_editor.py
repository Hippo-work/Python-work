import streamlit as st
import os
import json
import sys
from time import sleep
import pandas as pd
from config.dict_utils import save_script_json

st.write("Script Argument Editor")

#import json to edit
uploaded_file = st.selectbox("Pick Json to edit:", ["scripts/scripts.json", "plugins/plugins.json"], key="select")
st.write(uploaded_file)
if uploaded_file:
    with open(uploaded_file, "r") as f_in:
        scripts = json.load(f_in)
    st.success("File loaded successfully!")

st.write(scripts["repack"])
#schema render
def render_field(key, value):
    if isinstance(value, bool):
        return st.checkbox(key, value)
    elif isinstance(value, int):
        return st.number_input(key, value)
    elif isinstance(value, list):
        return st.text_area(key, json.dumps(value))
    else:
        return st.text_input(key, value)


#edit script
edited_scripts = {}
for script in scripts.items():
    new_value = st.text_input(f"{script}", key=script)
    edited_scripts[script] = new_value

#save value
if st.button("Save Edited JSON"):
    with open(uploaded_file, "w") as f:
        json.dump(edited_scripts, f, indent=4)

#for adding subprocesses together
#first selectbox 
#####################################################################################
def render_stage(name, fields):
    st.subheader(name)
    return {f: st.text_input(f) for f in fields}


_1 = st.selectbox("yes or no", [None, True, False], key="1")
if _1 == True:
    file_input = st.text_input("Input", key="Input")
    file_output = st.text_input("Output", key="Output")
    st.button("hi")
    _2 = st.selectbox("stage 2?", [None, True, False], key= "2")
    if _2 == True:
        Arg1 = st.text_input("Argument 1", key="Arg1")
        Arg2 = st.text_input("Argument 2", key="Arg2")
        _3 = st.selectbox("Stage 3?", [None, True, False], key="3")
        if _3 == True:
            Arg3 = st.text_input("Argument 3", key="Arg3")
            Arg4 = render_stage("Argument 4", ["yes, no"])
sub = st.button("Hi", key="Submit")
STAGES = {
    "Stage 1": ["Input", "Output"],
    "Stage 2": ["Argument 1", "Argument 2"],
    "Stage 3": ["Argument 3", "Argument 4"]
}



with st.form("script"):
    responses = {}
    for stage, fields in STAGES.items():
        if st.selectbox(f"Enable {stage}?", ["No", "Yes"]) == "Yes":
            responses[stage] = render_stage(stage, fields)
    submitted = st.form_submit_button("Submit")
