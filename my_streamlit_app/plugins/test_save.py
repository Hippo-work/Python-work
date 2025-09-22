# plugins/randomizer_tool.py
import sys
import os
import streamlit as st

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

class Test_save(Plugin):
    def __init__(self):
        self.name = "Tester"
        self.icon = "✂️"
        self.category = "DSP"

    def render(self, shared_state):
        st.subheader(f"{self.icon} {self.name}")
        # Your randomizer UI here
        st.write(" test ")
