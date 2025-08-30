from time import sleep
import streamlit as st
import pandas as pd
import os, importlib.util
import sys
import json
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from config.dict_utils import load_dict, save_dict, append_dict  # or paste the functions directly

### Resets text boxes
if "new_plugin" not in st.session_state:
    st.session_state["new_plugin"] = ""
if "new_module" not in st.session_state:
    st.session_state["new_module"] = ""
if "new_cl" not in st.session_state:
    st.session_state["new_cl"] = ""
if "remove_confirm" not in st.session_state:
    st.session_state["remove_confirm"] = ""


# --- Load dictionary from file ---
if "dict_df" not in st.session_state:
    with open("plugins/plugins.json", "r") as f:
        data = json.load(f)
        if data:
            st.session_state.dict_df = load_dict("plugins/plugins.json")
        else:
            data = {
                "Empty": {
                    "module": "Empty",
                    "class": "Empty"
                }
            }            
            with open("plugins/plugins.json", "w") as f:
                json.dump(data, f, indent=4)
            st.rerun()

#load blacklist
if "black_dict_df" not in st.session_state:
    with open("plugins/plugins_blacklist.json", "r") as f:
        data = json.load(f)
        if data:
            st.session_state.black_dict_df = load_dict("plugins/plugins_blacklist.json")
        else:
            data = {
                "Empty": {
                    "module": "Empty",
                    "class": "Empty"
                }
            }            
            with open("plugins/plugins_blacklist.json", "w") as f:
                json.dump(data, f, indent=4)
            st.rerun()



tab1, tab2, tab3, tab4 = st.tabs(["List of Processes", "Loaded Processes", "Add/Remove", "Blacklist"])

### Page 1
with tab1:
    st.subheader("List of processes")
    # page code here

    # --- Display and search ---
    st.title("📖 Sub Modules")
    search_term = st.text_input("🔍 Search dictionary", "")

    #sort
    sort_column = st.selectbox("Sort by column", ["Plugin", "Module", "Class"])
    sort_order = st.radio("Sort order", ["A → Z", "Z → A"])
    ascending = sort_order == "A → Z"
    sorted_df = st.session_state.dict_df.sort_values(by=sort_column, ascending=ascending)
    # st.dataframe(sorted_df, use_container_width=True)

    #load table
    filtered_df = st.session_state.dict_df[
        st.session_state.dict_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
    ]
    combined_df = filtered_df.sort_values(by=sort_column, ascending=ascending)
    st.dataframe(combined_df, use_container_width=True)


with tab2:
    from plugins.plugin_base import Plugin

    def load_plugins():
        plugins = []
        save_to_json = {}

        #check blacklist
        blacklist_path = "plugins/plugins_blacklist.json"
        if os.path.exists(blacklist_path):
            with open(blacklist_path, "r") as f:
                blacklist = set(json.load(f))
        
        else:
            blacklist = set()

        for filename in os.listdir("plugins"):
            if filename.endswith(".py"): #need to generic this for different types
                module_name = filename[:-3]
                path = os.path.join("plugins", filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, Plugin) and obj != Plugin and attr not in blacklist:
                        plugins.append(obj())

                        #save plugin to json
                        save_to_json[attr] = {
                            "module": f"plugins.{module_name}",
                            "class": attr
                        }
        with open("plugins/plugins.json", "w") as f:
            json.dump(save_to_json, f, indent=2)
        return plugins

    plugins = load_plugins()
    for plugin in plugins:
        with st.expander(f"{plugin.icon} {plugin.name}"):
            st.write("Category: ", plugin.category)
            plugin.render(st.session_state)


### Page 3
with tab3:
    st.subheader("Add / Remove from List")
    # page code here

    # --- Add Entry ---
    st.subheader("➕ Add or Edit Entry")
    new_plugin = st.text_input("New Plugin Name", key="new_plugin")
    new_module = st.text_input("New Module", key="new_module")
    new_cl = st.text_input("New Class", key="new_cl")

    #button press
    if st.button("Add Entry"):
        if new_plugin and new_module and new_cl:
            #add to data
            new_row = pd.DataFrame([[new_plugin, new_module, new_cl]], columns=["Plugin", "Module", "Class"])
            st.session_state.dict_df = pd.concat([st.session_state.dict_df, new_row], ignore_index=True)
            save_dict(st.session_state.dict_df)

            #fancy popup
            st.success(f"Added: {new_plugin} → {new_module} → {new_cl}")
            st.toast("✅ Entry added successfully!", icon="📘")

            #removes session states so that text boxes empty
            st.session_state.pop("new_plugin", None)
            st.session_state.pop("new_module", None)
            st.session_state.pop("new_cl", None)

            #re-runs script to update table
            sleep(5)
            st.rerun()

        else:
            st.warning("Please enter a Plugin Name, Module and Class.")

    # --- Remove Entry ---
    st.subheader("🗑️ Remove Entry / Blacklist")
    # Get key to remove
    remove_key = st.selectbox("Select key to remove", st.session_state.dict_df["Plugin"], key="remove_key")
    remove_confirm = st.text_input("Type CONFIRM to remove",key="remove_confirm")
    #double check on button press
    if remove_confirm == "CONFIRM":
        if st.button("Remove Entry"):
            #remove key
            
            append_dict(st.session_state.dict_df[st.session_state.dict_df["Plugin"] == remove_key], "plugins/plugins_blacklist.json")
            st.session_state.dict_df = st.session_state.dict_df[st.session_state.dict_df["Plugin"] != remove_key]
            save_dict(st.session_state.dict_df)
            

            #popup
            st.success(f"Removed: {remove_key}")

            #remove CONFIRM text and restart
            st.session_state.pop("remove_confirm", None)
            st.rerun()

with tab4:
    # --- Display and search ---
    st.title("⚫ Blacklist Processes")

    #load table
    black_df = st.session_state.black_dict_df[
        st.session_state.black_dict_df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().to_string(), axis=1)
    ]
    st.dataframe(black_df, use_container_width=True)

    #remove from blacklist
    available_blacklist = st.session_state.black_dict_df["Plugin"]
    remove_black_key = st.selectbox("Select key to remove", available_blacklist, key="black_key")
    if st.button("Remove blacklist Entry"):
        # Load blacklist from JSON
        with open("plugins/plugins_blacklist.json", "r") as f:
            blacklist = json.load(f)

        # Remove the selected key
        if remove_black_key in blacklist:
            del blacklist[remove_black_key]

            # Save updated blacklist
            with open("plugins/plugins_blacklist.json", "w") as f:
                json.dump(blacklist, f, indent=2)

            st.success(f"Blacklist Removed: {remove_black_key}")
            sleep(3)
            st.session_state.pop("black_dict_df", None)
            st.rerun()
        else:
            st.warning(f"{remove_black_key} not found in blacklist.")   


