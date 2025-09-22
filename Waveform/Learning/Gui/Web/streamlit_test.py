import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("BPSK Constellation Viewer")

# Simulate BPSK
bits = np.random.randint(0, 2, 100)
symbols = 2*bits - 1 + 0.1*np.random.randn(100)

fig, ax = plt.subplots()
ax.plot(np.real(symbols), np.imag(symbols), 'o')
ax.set_title("Constellation Plot")
st.pyplot(fig)

st.write("Hello World")