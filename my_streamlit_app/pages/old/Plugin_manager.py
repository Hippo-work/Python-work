import os, importlib.util
import sys
import streamlit as st
import json
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

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
        if filename.endswith(".py"):
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