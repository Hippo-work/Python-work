import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("DSP Visualizer 📡")

# Simulate a signal
fs = 1000
t = np.linspace(0, 1, fs)
signal = np.sin(2 * np.pi * 5 * t)

fig, ax = plt.subplots()
ax.plot(t, signal)
ax.set_title("5 Hz Sine Wave")
st.pyplot(fig)
