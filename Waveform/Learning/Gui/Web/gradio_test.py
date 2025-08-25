import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

def plot_waveform(freq):
    t = np.linspace(0, 1, 1000)
    y = np.sin(2 * np.pi * freq * t)
    fig, ax = plt.subplots()
    ax.plot(t, y)
    return fig

demo = gr.Interface(fn=plot_waveform, inputs=gr.Slider(1, 100), outputs="plot")
demo.launch()