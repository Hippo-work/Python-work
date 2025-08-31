# plugins/randomizer_tool.py
import sys
import os
import streamlit as st
import json

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

class Bit_Packer(Plugin):
    def __init__(self):
        self.name = "Unpack Bits"
        self.icon = "🤐"
        self.category = "DSP"

    def render(self, shared_state):
        st.subheader(f"{self.icon} {self.name}")
        # Your randomizer UI here
        st.write(" Description for unpack bits ")

    def unpack_bits(byte_arr:bytearray) -> list:
        # print("--unpack_bits--")
        # print("Reading bits from byte array:")
        #create a list to hold the bits
        bits = []
        for byte_index, byte in enumerate(byte_arr):
            for bit_index in range(8):
                bit = (byte >> (7 - bit_index)) & 1
                bits.append(bit)
        return bits
    
    def pack_bits(bits: list) -> bytearray:
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

if __name__ == "__main__":
    print(f" Bit packer", sys.argv)
    func = sys.argv[-3]  # e.g. "greet" or "compute"
    
    if func == "unpack_bits":
        file_path_in = sys.argv[-2]  # remaining arguments
        file_path_out = sys.argv[-1]
        with open(file_path_in, "rb") as f:
            buffers = bytearray(f.read())
        result = Bit_Packer.unpack_bits(buffers)
        result = bytearray(result)
        with open(file_path_out, "wb") as f_out:
            f_out.write(result)
        print("Unpack Complete")

        # print(json.dumps(result))
        # result = Bit_Packer.unpack_bits(buffers)
        # with open(file_path_out, "wb") as f_out:
        #     f_out.write(result)

    elif func == "pack_bits":
        file_path_in = sys.argv[-2]
        file_path_out = sys.argv[-1]
        with open(file_path_in, "rb") as f_in:
            bit_list = list(f_in.read())
        result = Bit_Packer.pack_bits(bit_list)
        with open(file_path_out, "wb") as f_out:
            f_out.write(result)
        print("Pack Complete")
