import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import spectrogram
from matplotlib.widgets import Slider

def generate_fsk_waveform(data, fs=1000, f0=100, f1=200, bit_duration=0.1):
    """
    Generate FSK-modulated waveform from binary data.
    :param data: List or array of 0s and 1s
    :param fs: Sampling frequency
    :param f0: Frequency for bit 0
    :param f1: Frequency for bit 1
    :param bit_duration: Duration of each bit in seconds
    :return: time array, waveform array
    """
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

# Example data sequence
data = [1, 0, 1, 1, 0, 0, 1]

# Generate FSK waveform
t_fsk, modulated_waveform = generate_fsk_waveform(data)

# Generate FM waveform
t_fm, fm_waveform = generate_fm_waveform(duration=len(modulated_waveform)/1000, fs=1000, f_carrier=10, f_mod=3, mod_index=2)

# Compute spectrograms
fs = 1000
f_fsk, tt_fsk, Sxx_fsk = spectrogram(modulated_waveform, fs)
f_fm, tt_fm, Sxx_fm = spectrogram(fm_waveform, fs)

# Compute power spectra (DFT magnitude)
freqs_fsk = np.fft.rfftfreq(len(modulated_waveform), d=1/fs)
power_spectrum_fsk = np.abs(np.fft.rfft(modulated_waveform))**2

freqs_fm = np.fft.rfftfreq(len(fm_waveform), d=1/fs)
power_spectrum_fm = np.abs(np.fft.rfft(fm_waveform))**2

# Create a figure with five subplots
fig = plt.figure(figsize=(28, 14))

# 1. Time domain plot (FSK)
ax1 = fig.add_subplot(2, 3, 1)
ax1.plot(t_fsk, modulated_waveform)
ax1.set_title("FSK-Modulated Waveform (Time Domain)")
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Amplitude")

# 2. 2D spectrogram plot (FSK)
ax2 = fig.add_subplot(2, 3, 2)
pcm = ax2.pcolormesh(tt_fsk, f_fsk, 10 * np.log10(Sxx_fsk), shading='gouraud', cmap='viridis')
ax2.set_title("2D Spectrogram of FSK Waveform")
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Frequency [Hz]")
fig.colorbar(pcm, ax=ax2, label='Power [dB]')

# 3. Power spectrum plot (FSK)
ax3 = fig.add_subplot(2, 3, 3)
ax3.plot(freqs_fsk, 10 * np.log10(power_spectrum_fsk))
ax3.set_title("Power Spectrum (FSK DFT Magnitude)")
ax3.set_xlabel("Frequency [Hz]")
ax3.set_ylabel("Power [dB]")

# 4. 3D spectrogram plot (FSK)
ax4 = fig.add_subplot(2, 3, 4, projection='3d')
T_fsk, F_fsk = np.meshgrid(tt_fsk, f_fsk)
ax4.plot_surface(T_fsk, F_fsk, 10 * np.log10(Sxx_fsk), cmap='viridis')
ax4.set_xlabel('Time [s]')
ax4.set_ylabel('Frequency [Hz]')
ax4.set_zlabel('Power [dB]')
ax4.set_title('3D Spectrogram of FSK Waveform')

# 5. Power spectrum plot (FM)
ax5 = fig.add_subplot(2, 3, 5)
ax5.plot(freqs_fm, 10 * np.log10(power_spectrum_fm))
ax5.set_title("Power Spectrum (FM DFT Magnitude)")
ax5.set_xlabel("Frequency [Hz]")
ax5.set_ylabel("Power [dB]")

plt.tight_layout()

# Create sliders for FSK f0, FSK f1, FM mod_index
axcolor = 'lightgoldenrodyellow'
ax_f0 = plt.axes([0.15, 0.92, 0.2, 0.03], facecolor=axcolor)
ax_f1 = plt.axes([0.45, 0.92, 0.2, 0.03], facecolor=axcolor)
ax_mod = plt.axes([0.75, 0.92, 0.2, 0.03], facecolor=axcolor)

s_f0 = Slider(ax_f0, 'FSK f0', 50, 300, valinit=100)
s_f1 = Slider(ax_f1, 'FSK f1', 100, 400, valinit=200)
s_mod = Slider(ax_mod, 'FM Index', 0.5, 10, valinit=2)

def update(val):
    f0 = s_f0.val
    f1 = s_f1.val
    mod_index = s_mod.val
    t_fsk, modulated_waveform = generate_fsk_waveform(data, fs=fs, f0=f0, f1=f1, bit_duration=0.1)
    t_fm, fm_waveform = generate_fm_waveform(duration=len(modulated_waveform)/fs, fs=fs, f_carrier=10, f_mod=3, mod_index=mod_index)
    f_fsk, tt_fsk, Sxx_fsk = spectrogram(modulated_waveform, fs)
    freqs_fsk = np.fft.rfftfreq(len(modulated_waveform), d=1/fs)
    power_spectrum_fsk = np.abs(np.fft.rfft(modulated_waveform))**2
    freqs_fm = np.fft.rfftfreq(len(fm_waveform), d=1/fs)
    power_spectrum_fm = np.abs(np.fft.rfft(fm_waveform))**2

    # Update plots
    ax1.clear()
    ax1.plot(t_fsk, modulated_waveform)
    ax1.set_title("FSK-Modulated Waveform (Time Domain)")
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Amplitude")

    ax2.clear()
    pcm = ax2.pcolormesh(tt_fsk, f_fsk, 10 * np.log10(Sxx_fsk), shading='gouraud', cmap='viridis')
    ax2.set_title("2D Spectrogram of FSK Waveform")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Frequency [Hz]")

    ax3.clear()
    ax3.plot(freqs_fsk, 10 * np.log10(power_spectrum_fsk))
    ax3.set_title("Power Spectrum (FSK DFT Magnitude)")
    ax3.set_xlabel("Frequency [Hz]")
    ax3.set_ylabel("Power [dB]")

    ax4.clear()
    T_fsk, F_fsk = np.meshgrid(tt_fsk, f_fsk)
    ax4.plot_surface(T_fsk, F_fsk, 10 * np.log10(Sxx_fsk), cmap='viridis')
    ax4.set_xlabel('Time [s]')
    ax4.set_ylabel('Frequency [Hz]')
    ax4.set_zlabel('Power [dB]')
    ax4.set_title('3D Spectrogram of FSK Waveform')

    ax5.clear()
    ax5.plot(freqs_fm, 10 * np.log10(power_spectrum_fm))
    ax5.set_title("Power Spectrum (FM DFT Magnitude)")
    ax5.set_xlabel("Frequency [Hz]")
    ax5.set_ylabel("Power [dB]")

    fig.canvas.draw_idle()

s_f0.on_changed(update)
s_f1.on_changed(update)
s_mod.on_changed(update)

plt.show()