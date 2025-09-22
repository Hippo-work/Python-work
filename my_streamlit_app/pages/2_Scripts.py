from time import sleep
import streamlit as st
import pandas as pd
import os, importlib.util
import sys
import json
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from config.dict_utils import load_script_json, save_script_json, append_script_json  # or paste the functions directly

### Resets text boxes
if "new_script" not in st.session_state:
    st.session_state["new_script"] = ""
if "new_module" not in st.session_state:
    st.session_state["new_module"] = ""
if "remove_confirm" not in st.session_state:
    st.session_state["remove_confirm"] = ""


# --- Load dictionary from file ---
if "script_dict_df" not in st.session_state:
    with open("scripts/scripts.json", "r") as f:
        data = json.load(f)
        if data:
            st.session_state.script_dict_df = load_script_json("scripts/scripts.json")
        else:
            data = {
                "Empty": {
                    "module": "Empty",
                    "arguments": "Empty",
                }
            }            
            with open("scripts/scripts.json", "w") as f:
                json.dump(data, f, indent=4)
            st.rerun()

#load blacklist
if "black_script_dict_df" not in st.session_state:
    with open("scripts/scripts_blacklist.json", "r") as f:
        data = json.load(f)
        if data:
            st.session_state.black_script_dict_df = load_script_json("scripts/scripts_blacklist.json")
        else:
            data = {
                "Empty": {
                    "module": "Empty",
                    "arguments": "Empty"
                }
            }            
            with open("scripts/scripts_blacklist.json", "w") as f:
                json.dump(data, f, indent=4)
            st.rerun()



tab1, tab3, tab4 = st.tabs(["List of Scripts", "Add/Remove", "Blacklist"])

### Page 1
with tab1:
    st.subheader("List of Scripts")
    # page code here

    # --- Display and search ---
    st.title("📖 Demod Scripts")
    search_term = st.text_input("🔍 Search", "")
    # st.write("Available columns:", st.session_state.script_dict_df.columns)

    #sort
    sort_column = st.selectbox("Sort by column", ["Scripts", "Module"])
    sort_order = st.radio("Sort order", ["A → Z", "Z → A"])
    ascending = sort_order == "A → Z"
    sorted_df = st.session_state.script_dict_df.sort_values(by=sort_column, ascending=ascending)
    # st.dataframe(sorted_df, use_container_width=True)

    #load table
    filtered_df = st.session_state.script_dict_df[
        st.session_state.script_dict_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
    ]
    combined_df = filtered_df.sort_values(by=sort_column, ascending=ascending)
    st.dataframe(combined_df, use_container_width=True)


with tab3:
    def load_script():
        current_list = st.session_state.script_dict_df
        blacklist_path = "scripts/scripts_blacklist.json"
        existing_path = "scripts/scripts.json"

        # Load existing scripts.json if it exists
        if os.path.exists(existing_path):
            with open(existing_path, "r") as f:
                save_to_json = json.load(f)
        else:
            save_to_json = {}

        # Load blacklist
        if os.path.exists(blacklist_path):
            with open(blacklist_path, "r") as f:
                blacklist_dict = json.load(f)
                blacklist = set(blacklist_dict.keys())
        else:
            blacklist = set()

        # Scan for new scripts
        for filename in os.listdir("scripts"):
            if filename.endswith(".sh"):
                script_name = filename[:-3]
                path = os.path.join("scripts", filename)

                if script_name in blacklist or script_name in current_list:
                    continue

                if script_name not in save_to_json:
                    save_to_json[script_name] = {
                        "module": path,
                        "arguments": "Empty"
                    }

        # Save updated dictionary
        with open(existing_path, "w") as f:
            json.dump(save_to_json, f, indent=2)


    scripts = load_script()

### Page 3
# with tab3:
    st.subheader("Add / Remove from List")
    # page code here

    # --- Add Entry ---
    st.subheader("➕ Add or Edit Entry")
    new_script = st.text_input("New Script Name", key="new_script")
    new_module = st.text_input("New Module", key="new_module")
    new_arguments = st.text_input("New Arguments", key="new_arguments")

    #button press
    if st.button("Add Entry"):
        if new_script and new_module:
            #add to data
            new_row = pd.DataFrame([[new_script, new_module, new_arguments]], columns=["Scripts", "Module", "Arguments"])
            st.session_state.script_dict_df = pd.concat([st.session_state.script_dict_df, new_row], ignore_index=True)
            save_script_json(st.session_state.script_dict_df)

            #fancy popup
            st.success(f"Added: {new_script} → {new_module}")
            st.toast("✅ Entry added successfully!", icon="📘")

            #removes session states so that text boxes empty
            st.session_state.pop("new_script", None)
            st.session_state.pop("new_module", None)

            #re-runs scripts to update table
            sleep(5)
            st.rerun()

        else:
            st.warning("Please enter a Script Name, Module and Class.")

    # --- Remove Entry ---
    st.subheader("🗑️ Remove Entry / Blacklist")
    # Get key to remove
    remove_key = st.selectbox("Select key to remove", st.session_state.script_dict_df["Scripts"], key="remove_key")
    remove_confirm = st.text_input("Type CONFIRM to remove",key="remove_confirm")
    #double check on button press
    if remove_confirm == "CONFIRM":
        if st.button("Remove Entry"):
            #remove key
            
            append_script_json(st.session_state.script_dict_df[st.session_state.script_dict_df["Scripts"] == remove_key], "scripts/scripts_blacklist.json")
            st.session_state.script_dict_df = st.session_state.script_dict_df[st.session_state.script_dict_df["Scripts"] != remove_key]
            save_script_json(st.session_state.script_dict_df)
            

            #popup
            st.success(f"Removed: {remove_key}")

            #remove CONFIRM text and restart
            st.session_state.pop("remove_confirm", None)
            st.rerun()

with tab4:
    # --- Display and search ---
    st.title("⚫ Blacklist Scripts")

    #load table
    black_df = st.session_state.black_script_dict_df[
        st.session_state.black_script_dict_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
    ]
    st.dataframe(black_df, use_container_width=True)

    #remove from blacklist
    available_blacklist = st.session_state.black_script_dict_df["Scripts"]
    remove_black_key = st.selectbox("Select key to remove", available_blacklist, key="black_key")
    if st.button("Remove blacklist Entry"):
        # Load blacklist from JSON
        with open("scripts/scripts_blacklist.json", "r") as f:
            blacklist = json.load(f)

        # Remove the selected key
        if remove_black_key in blacklist:
            del blacklist[remove_black_key]

            # Save updated blacklist
            with open("scripts/scripts_blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=2)

            st.success(f"Blacklist Removed: {remove_black_key}")
            sleep(3)
            st.session_state.pop("black_script_dict_df", None)
            st.rerun()
        else:
            st.warning(f"{remove_black_key} not found in blacklist.")   


