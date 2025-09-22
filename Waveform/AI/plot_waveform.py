import matplotlib.pyplot as plt
from dft_waveform import generate_fm_waveform, compute_dft

# Generate FM waveform
t, waveform = generate_fm_waveform(duration=1.0, fs=1000, f_carrier=5, f_mod=2, mod_index=2)

# Compute DFT
freq, dft_mag = compute_dft(waveform)

# Plot time-domain waveform
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(t, waveform)
plt.title("FM Waveform (Time Domain)")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot frequency spectrum
plt.subplot(1, 2, 2)
plt.plot(freq, dft_mag)
plt.title("DFT Magnitude Spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.tight_layout()
plt.show()