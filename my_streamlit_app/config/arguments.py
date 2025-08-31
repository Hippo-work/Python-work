import streamlit as st

def render_argument_form(script_name, schema):
    st.subheader(f"Arguments for `{script_name}`")
    user_inputs = {}

    for arg, props in schema.items():
        label = props.get("label", arg)
        default = props.get("default")

        if props["type"] == "str":
            user_inputs[arg] = st.text_input(label, value=default)
        elif props["type"] == "int":
            user_inputs[arg] = st.number_input(label, value=default, step=1)
        elif props["type"] == "float":
            user_inputs[arg] = st.number_input(label, value=default)
        elif props["type"] == "bool":
            user_inputs[arg] = st.checkbox(label, value=default)

    return user_inputs