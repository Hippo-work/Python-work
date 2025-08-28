# plugins/test.py
import sys
import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from plugins.plugin_base import Plugin

class Matplot_Test(Plugin):
    def __init__(self):
        self.name = "Matplot Test"
        self.icon = "📈"
        self.category = "DSP"

    def render(self, shared_state):
        st.subheader(f"{self.icon} {self.name}")
        # Your randomizer UI here
        # Simulate a signal
        fs = 1000
        t = np.linspace(0, 1, fs)
        signal = np.sin(2 * np.pi * 5 * t)

        fig, ax = plt.subplots()
        ax.plot(t, signal)
        ax.set_title("5 Hz Sine Wave")
        st.pyplot(fig)