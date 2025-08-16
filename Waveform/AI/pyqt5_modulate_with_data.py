import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider
)
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from scipy.signal import spectrogram

def generate_fsk_waveform(data, fs=1000, f0=100, f1=200, bit_duration=0.1):
    t = np.arange(0, bit_duration * len(data), 1/fs)
    waveform = np.zeros_like(t)
    for i, bit in enumerate(data):
        freq = f1 if bit else f0
        idx_start = int(i * bit_duration * fs)
        idx_end = int((i + 1) * bit_duration * fs)
        waveform[idx_start:idx_end] = np.cos(2 * np.pi * freq * t[idx_start:idx_end])
    return t, waveform

def generate_fm_waveform(duration=1.0, fs=1000, f_carrier=10, f_mod=3, mod_index=2):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    waveform = np.cos(2 * np.pi * f_carrier * t + mod_index * np.sin(2 * np.pi * f_mod * t))
    return t, waveform

class ModulateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FSK & FM Modulation Viewer (PyQt5)")
        self.setGeometry(100, 100, 1200, 700)

        self.fs = 1000
        self.data = [1, 0, 1, 1, 0, 0, 1]

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Controls
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # FSK f0 slider
        control_layout.addWidget(QLabel("FSK f0:"))
        self.fsk_f0_slider = QSlider(Qt.Horizontal)
        self.fsk_f0_slider.setMinimum(50)
        self.fsk_f0_slider.setMaximum(300)
        self.fsk_f0_slider.setValue(100)
        self.fsk_f0_slider.setTickInterval(10)
        self.fsk_f0_slider.valueChanged.connect(self.update_plot)
        control_layout.addWidget(self.fsk_f0_slider)

        # FSK f1 slider
        control_layout.addWidget(QLabel("FSK f1:"))
        self.fsk_f1_slider = QSlider(Qt.Horizontal)
        self.fsk_f1_slider.setMinimum(100)
        self.fsk_f1_slider.setMaximum(400)
        self.fsk_f1_slider.setValue(200)
        self.fsk_f1_slider.setTickInterval(10)
        self.fsk_f1_slider.valueChanged.connect(self.update_plot)
        control_layout.addWidget(self.fsk_f1_slider)

        # FM Index slider
        control_layout.addWidget(QLabel("FM Index:"))
        self.fm_index_slider = QSlider(Qt.Horizontal)
        self.fm_index_slider.setMinimum(5)
        self.fm_index_slider.setMaximum(100)
        self.fm_index_slider.setValue(20)
        self.fm_index_slider.setTickInterval(1)
        self.fm_index_slider.valueChanged.connect(self.update_plot)
        control_layout.addWidget(self.fm_index_slider)

        # Matplotlib Figure and Canvas
        self.fig = Figure(figsize=(12, 6), dpi=100)
        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 3)
        self.ax4 = self.fig.add_subplot(2, 2, 4)
        self.canvas = FigureCanvasQTAgg(self.fig)
        main_layout.addWidget(self.canvas)

        self.update_plot()

    def update_plot(self):
        f0 = self.fsk_f0_slider.value()
        f1 = self.fsk_f1_slider.value()
        mod_index = self.fm_index_slider.value() / 10.0  # scale to 0.5-10

        # FSK
        t_fsk, modulated_waveform = generate_fsk_waveform(self.data, fs=self.fs, f0=f0, f1=f1, bit_duration=0.1)
        freqs_fsk = np.fft.rfftfreq(len(modulated_waveform), d=1/self.fs)
        power_spectrum_fsk = np.abs(np.fft.rfft(modulated_waveform))**2

        # FM
        t_fm, fm_waveform = generate_fm_waveform(duration=len(modulated_waveform)/self.fs, fs=self.fs, f_carrier=10, f_mod=3, mod_index=mod_index)
        freqs_fm = np.fft.rfftfreq(len(fm_waveform), d=1/self.fs)
        power_spectrum_fm = np.abs(np.fft.rfft(fm_waveform))**2

        # Clear axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Time domain (FSK)
        self.ax1.plot(t_fsk, modulated_waveform)
        self.ax1.set_title("FSK-Modulated Waveform (Time Domain)")
        self.ax1.set_xlabel("Time [s]")
        self.ax1.set_ylabel("Amplitude")

        # Power spectrum (FSK)
        self.ax2.plot(freqs_fsk, 10 * np.log10(power_spectrum_fsk))
        self.ax2.set_title("Power Spectrum (FSK DFT Magnitude)")
        self.ax2.set_xlabel("Frequency [Hz]")
        self.ax2.set_ylabel("Power [dB]")

        # Time domain (FM)
        self.ax3.plot(t_fm, fm_waveform)
        self.ax3.set_title("FM-Modulated Waveform (Time Domain)")
        self.ax3.set_xlabel("Time [s]")
        self.ax3.set_ylabel("Amplitude")

        # Power spectrum (FM)
        self.ax4.plot(freqs_fm, 10 * np.log10(power_spectrum_fm))
        self.ax4.set_title("Power Spectrum (FM DFT Magnitude)")
        self.ax4.set_xlabel("Frequency [Hz]")
        self.ax4.set_ylabel("Power [dB]")

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModulateApp()
    window.show()
    sys.exit(app.exec_())