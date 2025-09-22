import streamlit as st
import io
import xml.etree.ElementTree as ET
import sys

from st_Bitops.bit_delta import delta_bits
from st_Bitops.read_bits import *

#xml load
tree = ET.parse("DSP.xml")
root = tree.getroot()
select_options = [opt.text for opt in root.findall("option")]

#st start
st.set_page_config(page_title="DSP File Processor", layout="centered")
st.title("📁 DSP File Processor")

# Step 1: Upload a file
uploaded_file = st.file_uploader("Upload your input file")

if uploaded_file:
    st.success("File uploaded successfully!")

    # Step 2: Process the file
    st.subheader("🔧 Processing Options")
    selected = st.multiselect("Choose a demod:", select_options)
    if selected:
        st.write(f"You selected: {selected[0]}")

    # process = st.selectbox("Choose a Demod", select_options)
    process_button = st.button("Run DSP Processing")

    if process_button:
        # Example: Read file contents
        input_bytes = uploaded_file.read()

        # Replace this with your DSP logic
        if "bit_delta" in selected:
            delta_bits = delta_bits(input_bytes)
            packed = pack_bits(delta_bits)
            processed_bytes = packed

        # Replace this with your DSP logic
        if "read_bits" in selected:
            unpack = unpack_bits(input_bytes)
            pack = pack_bits(unpack)
            processed_bytes = pack

        st.success("Processing complete!")

        # Step 3: Download the result
        ### cant accept bytesarray
        st.download_button(
            label="Download Processed File",
            data=bytes(processed_bytes),
            file_name="processed_output.bin",
            mime="application/octet-stream"
        )