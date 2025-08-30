# plugins/base.py
import sys
import os
import streamlit as st

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

class Write_Bytes(Plugin):
    def __init__(self):
        self.name = "Write Bytes"
        self.icon = "✂️"
        self.category = "Tool"

    def render(self, shared_state):
        st.subheader(f"{self.icon} {self.name}")
        # Your randomizer UI here
        st.write(" Description for Write Bytes here ")
        
    def write(self, file_path_in, file_path_out):
        buffers = []
        with open(file_path_in, 'rb') as f:
            buffers.append(bytearray(f.read()))
        with open(file_path_out, 'wb') as file:
            file.write((buffers[0]))

    def write_stdout(self, file_path_out):
        with open(file_path_out, 'wb') as file:
            file.write((file))

if __name__ == "__main__":
    # print(sys.argv)
    func = sys.argv[-3]  # e.g. "greet" or "compute"
    file_path_in = sys.argv[-2]  # remaining arguments
    file_path_out = sys.argv[-1]
    
    Write_Bytes.write(func,file_path_in,file_path_out)
    print("File out.bit written")
    
    # processor = Write_Bytes()

    # if hasattr(processor, func):
    #     method = getattr(processor, func)
    #     method(*args)
    # else:
    #     print(f"Write Function '{func}' not found.")