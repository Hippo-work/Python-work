from time import sleep
import streamlit as st
import pandas as pd
from dict_utils import load_dict, save_dict  # or paste the functions directly

### Resets text boxes
if "new_key" not in st.session_state:
    st.session_state["new_key"] = ""
if "new_value" not in st.session_state:
    st.session_state["new_value"] = ""
if "remove_confirm" not in st.session_state:
    st.session_state["remove_confirm"] = ""


# --- Load dictionary from file ---
if "dict_df" not in st.session_state:
    st.session_state.dict_df = load_dict()

tab1, tab2 = st.tabs(["List of Processes", "Add/Remove"])

### Page 1
with tab1:
    st.subheader("List of processes")
    # page code here

    # --- Display and search ---
    st.title("📖 Persistent Dictionary Editor")
    search_term = st.text_input("🔍 Search dictionary", "")

    #sort
    sort_column = st.selectbox("Sort by column", ["Key", "Value"])
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



### Page 2
with tab2:
    st.subheader("Add / Remove from List")
    # page code here

    # --- Add Entry ---
    st.subheader("➕ Add New Entry")
    new_key = st.text_input("New Key", key="new_key")
    new_value = st.text_input("New Value", key="new_value")

    #button press
    if st.button("Add Entry"):
        if new_key and new_value:
            #add to data
            new_row = pd.DataFrame([[new_key, new_value]], columns=["Key", "Value"])
            st.session_state.dict_df = pd.concat([st.session_state.dict_df, new_row], ignore_index=True)
            save_dict(st.session_state.dict_df)

            #fancy popup
            st.success(f"Added: {new_key} → {new_value}")
            st.toast("✅ Entry added successfully!", icon="📘")

            #removes session states so that text boxes empty
            st.session_state.pop("new_key", None)
            st.session_state.pop("new_value", None)

            #re-runs script to update table
            sleep(5)
            st.rerun()

        else:
            st.warning("Please enter both key and value.")

    # --- Remove Entry ---
    st.subheader("🗑️ Remove Entry")
    # Get key to remove
    remove_key = st.selectbox("Select key to remove", st.session_state.dict_df["Key"])
    remove_confirm = st.text_input("Type CONFIRM to remove",key="remove_confirm")
    #double check on button press
    if remove_confirm == "CONFIRM":
        if st.button("Remove Entry"):
            #remove key
            st.session_state.dict_df = st.session_state.dict_df[st.session_state.dict_df["Key"] != remove_key]
            save_dict(st.session_state.dict_df)

            #popup
            st.success(f"Removed: {remove_key}")

            #remove CONFIRM text and restart
            st.session_state.pop("remove_confirm", None)
            st.rerun()




