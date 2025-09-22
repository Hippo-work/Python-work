import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from dft_waveform import generate_fm_waveform

# Generate FM waveform
t, waveform = generate_fm_waveform(duration=1.0, fs=1000, f_carrier=5, f_mod=2, mod_index=2)

# Compute spectrogram
fs = 1000  # Sampling frequency
f, tt, Sxx = spectrogram(waveform, fs)

# Plot 2D spectrogram
plt.figure(figsize=(10, 6))
plt.pcolormesh(tt, f, 10 * np.log10(Sxx), shading='gouraud', cmap='viridis')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('2D Spectrogram of FM Waveform')
plt.colorbar(label='Power [dB]')
plt.tight_layout()
plt.show()