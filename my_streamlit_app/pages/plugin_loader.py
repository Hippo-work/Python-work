import streamlit as st
import json
import importlib
import sys
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

def load_plugins_from_json(json_path="plugins/plugins.json"):
    with open(json_path) as f:
        config = json.load(f)
    st.write(config)
    plugins = {}

    for name, meta in config.items():
        try:
            module = importlib.import_module(meta["module"])
            cls = getattr(module, meta["class"])
            instance = cls()
            plugins[name] = instance
        except Exception as e:
            print(f"Failed to load plugin '{name}': {e}")

    return plugins

st.write("This pulls in a json dictionary that converts to a python class module" \
"for a pointer to a python script, which is then ran")

plugins = load_plugins_from_json()
st.write("Loaded plugin:", plugins.keys())

plugins["Randomizer"].render(st.session_state)
