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

    def unpack_bits(byte_arr:bytearray) -> list:
        print("--unpack_bits--")
        print("Reading bits from byte array:")
        #create a list to hold the bits
        bits = []
        for byte_index, byte in enumerate(byte_arr):
            print(f"Byte {byte_index}: ", end="\n")
            for bit_index in range(8):
                # Shift right and mask with 1 to get the bit
                bit = (byte >> (7 - bit_index)) & 1
                print(bit, end=" ") 
                bits.append(bit)
                if __name__ == "__main__":
                    print(f"Bits so far: {bits}")  # Print the bits collected so far
            print()  # Newline after each byte
        print(f"Bit list: {bits}")
        return bits
    
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
