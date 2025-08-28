import streamlit as st

st.title("Multi Tabs 📡")

tab1, tab2, tab3 = st.tabs(["Tab1", "Tab 2", "Tab 3"])

with tab1:
    st.subheader("Tab 1")
    # Your waveform/FFT code here

with tab2:
    st.subheader("Tab 2")
    # Your FEC + BER simulation here

with tab3:
    st.subheader("Tab 3")
    # Your modulation visualizer here
