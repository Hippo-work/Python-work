'''
Spectral leakage occurs when a signal is not perfectly periodic 
over the sampled interval. Applying a window function to the signal
before performing the DFT can reduce leakage by smoothing the signal 
at the boundaries.
'''

import numpy as np
import matplotlib.pyplot as plt

# Step 1: Create a signal with spectral leakage
fs = 500  # Sampling frequency
T = 1/fs  # Sampling period
t = np.arange(0, 1, T)  # Time vector

# Frequencies of sinusoids
f1 = 50
f2 = 120
f3 = np.arange(50,120,5)
print(f3)

# Create signal: sum of two sinusoids
x = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

# Step 2: Apply a window function (Hamming window)
window = np.hamming(len(x))
x_windowed = x * window

# Step 3: Compute the DFT of the original and windowed signal
X = np.fft.fft(x)
X_windowed = np.fft.fft(x_windowed)

# Step 4: Frequency axis
frequencies = np.fft.fftfreq(len(x), T)

# Step 5: Plot the original and windowed signals
plt.figure(figsize=(12, 8))

# Plot the original signal and windowed signal
plt.subplot(3, 1, 1)
plt.plot(t, x, label='Original Signal')
plt.title('Original Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 2)
plt.plot(t, x_windowed, label='Windowed Signal', color='orange')
plt.title('Windowed Signal (Hamming Window)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# Plot the magnitude spectra
plt.subplot(3, 1, 3)
plt.plot(frequencies[:len(x)//2], np.abs(X)[:len(x)//2], label='Original Spectrum')
plt.plot(frequencies[:len(x)//2], np.abs(X_windowed)[:len(x)//2], label='Windowed Spectrum', color='orange')
plt.title('Frequency Domain Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.legend()

plt.tight_layout()
plt.show()