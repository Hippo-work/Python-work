# plugins/randomizer_tool.py
import sys
import os
import streamlit as st

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

class Unpack_Bits(Plugin):
    def __init__(self):
        self.name = "Unpack Bits"
        self.icon = "🤐"
        self.category = "DSP"

    def render(self, shared_state):
        st.subheader(f"{self.icon} {self.name}")
        # Your randomizer UI here
        st.write(" Description for unpack bits ")

    def pack_bits(bits: list) -> bytearray:
        """Packs a list of bits into a bytearray."""
        print("--pack_bits--")
        packed = bytearray()
        #pad the bits to make sure they are a multiple of 8
        while len(bits) % 8 != 0:
            bits.append(0)
        #checks if bits are already a bytearray
        if isinstance(bits, bytearray):
            raise TypeError("Input must be a list of bits, not a bytearray.")
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bits):
                    byte = (byte << 1) | bits[i + j]
            packed.append(byte)
        return packed