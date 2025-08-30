# plugins/randomizer_tool.py
import sys
import os
import streamlit as st
import io

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
        if isinstance(bits[0], list):
            truncated = bits[start:stop:1]
        if isinstance(bits[0], bytearray or bytes):
            truncated = bits[0][start:stop:1]
        return truncated
    
if __name__ == "__main__":
    print(sys.argv)
    func = sys.argv[-5] 
    file_path = sys.argv[-4]

    buffers = []
    with open(file_path, 'rb') as f:
                buffers.append(bytearray(f.read()))

    start = int(sys.argv[-3])
    stop = int(sys.argv[-2])
    file_path_out = sys.argv[-1]

    result = Truncate_Bits.truncate(buffers,start,stop)
    # file_path_out = "../test/tmp.bit"
    with open(file_path_out, "wb") as f_out:
         f_out.write(result)
    print("Truncate Complete")




    # if hasattr(processor, func):
    #     method = getattr(processor, func)
    #     method(start, stop)
    # else:
    #     print(f"Truncate Function '{func}' not found.")

