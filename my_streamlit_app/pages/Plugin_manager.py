import os, importlib.util
import sys
import streamlit as st
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

def load_plugins():
    plugins = []
    for filename in os.listdir("plugins"):
        if filename.endswith(".py"):
            path = os.path.join("plugins", filename)
            spec = importlib.util.spec_from_file_location(filename[:-3], path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, Plugin) and obj != Plugin:
                    plugins.append(obj())
    return plugins


plugins = load_plugins()
for plugin in plugins:
    with st.expander(f"{plugin.icon} {plugin.name}"):
        plugin.render(st.session_state)
