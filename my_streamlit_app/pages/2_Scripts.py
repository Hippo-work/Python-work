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
                }
            }            
            with open("scripts/scripts_blacklist.json", "w") as f:
                json.dump(data, f, indent=4)
            st.rerun()



tab1, tab2, tab3, tab4 = st.tabs(["List of Scripts", "Loaded Scripts", "Add/Remove", "Blacklist"])

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


with tab2:
    from scripts.script_base import Script

    def load_script():
        # scripts = []
        save_to_json = {}

        #check blacklist
        blacklist_path = "scripts/scripts_blacklist.json"
        if os.path.exists(blacklist_path):
            with open(blacklist_path, "r") as f:
                blacklist_dict = json.load(f)
                blacklist = set(blacklist_dict.keys())
        
        else:
            blacklist = set()

        for filename in os.listdir("scripts"):
            if filename.endswith(".sh"):
                path = os.path.join("scripts", filename)
                script_name = filename[:-3]  # Strip '.sh' extension
                if script_name in blacklist:
                    continue

                save_to_json[script_name] = {
                    "module": path
                }

        with open("scripts/scripts.json", "w") as f:
            json.dump(save_to_json, f, indent=2)

        return 


    scripts = load_script()
    # for script in scripts:
    #     with st.expander(f"{script.icon} {script.name}"):
    #         st.write("Category: ", script.category)
    #         script.render(st.session_state)


### Page 3
with tab3:
    st.subheader("Add / Remove from List")
    # page code here

    # --- Add Entry ---
    st.subheader("➕ Add or Edit Entry")
    new_script = st.text_input("New Script Name", key="new_script")
    new_module = st.text_input("New Module", key="new_module")

    #button press
    if st.button("Add Entry"):
        if new_script and new_module:
            #add to data
            new_row = pd.DataFrame([[new_script, new_module]], columns=["Scripts", "Module"])
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


