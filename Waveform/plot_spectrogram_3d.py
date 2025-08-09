import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import spectrogram
from dft_waveform import generate_fm_waveform

# Generate FM waveform
t, waveform = generate_fm_waveform(duration=1.0, fs=1000, f_carrier=5, f_mod=2, mod_index=2)

# Compute spectrogram
fs = 1000  # Sampling frequency
f, tt, Sxx = spectrogram(waveform, fs)

# Prepare meshgrid for 3D plotting
T, F = np.meshgrid(tt, f)

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')

# Use log scale for better visualization
ax.plot_surface(T, F, 10 * np.log10(Sxx), cmap='viridis')

ax.set_xlabel('Time [s]')
ax.set_ylabel('Frequency [Hz]')
ax.set_zlabel('Power [dB]')
ax.set_title('3D Spectrogram of FM Waveform')

plt.show()