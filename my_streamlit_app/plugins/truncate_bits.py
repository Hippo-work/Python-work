# plugins/randomizer_tool.py
import sys
import os
import streamlit as st

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

class Truncate_Bits(Plugin):
    def __init__(self):
        self.name = "Truncate Bits"
        self.icon = "✂️"
        self.category = "DSP"

    def render(self, shared_state):
        st.subheader(f"{self.icon} {self.name}")
        # Your randomizer UI here
        st.write(" Description for Truncate bits (maybe code) ")

    def truncate(bits, start=0, stop=None):
        #list slicing easy
        #stop is optional
        truncate = bits[start:stop:1]
        return truncate