import streamlit as st

def extract_fields(config):
    fields = []
    for section, content in config.items():
        for key, value in content.get("arguments", {}).items():
            fields.append({
                "section": section,
                "field": key,
                "value": value,
                "type": "text" if isinstance(value, str) else "number"
            })
    return fields

def render_form(config):
    st.header("Auto-Generated Form")
    updated_config = {}

    for section, content in config.items():
        st.subheader(f"Section: {section}")
        updated_args = {}
        for key, value in content.get("arguments", {}).items():
            input_type = "text" if isinstance(value, str) else "number"
            new_val = st.text_input(f"{key}", value) if input_type == "text" else st.number_input(f"{key}", value)
            updated_args[key] = str(new_val)
        updated_config[section] = {
            "module": content["module"],
            "arguments": updated_args
        }

    return updated_config

if st.button("Save Config"):
    new_config = render_form(config)
    st.json(new_config)