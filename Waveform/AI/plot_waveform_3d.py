import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from dft_waveform import generate_fm_waveform, compute_dft

# Generate FM waveform
t, waveform = generate_fm_waveform(duration=1.0, fs=1000, f_carrier=5, f_mod=2, mod_index=2)

# Compute DFT
freq, dft_mag = compute_dft(waveform)

# Prepare meshgrid for 3D plotting
T, F = np.meshgrid(t[:len(freq)], freq)
Z = np.tile(dft_mag, (len(t[:len(freq)]), 1)).T

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(T, F, Z, cmap='viridis')

ax.set_xlabel('Time [s]')
ax.set_ylabel('Frequency [Hz]')
ax.set_zlabel('DFT Magnitude')
ax.set_title('3D DFT Magnitude Surface')

plt.show()