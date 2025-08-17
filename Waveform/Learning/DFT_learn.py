import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate a sample signal (sum of two sinusoids)
fs = 500  # Sampling frequency (samples per second)
T = 1/fs  # Sampling period
t = np.arange(0, 1, T)  # Time vector

# Define two frequencies
f1 = 50  # Frequency of first sinusoid (Hz)
f2 = 120  # Frequency of second sinusoid (Hz)
f3 = 210

# Create the signal: sum of two sinusoids
x = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t) + np.sin(2 * np.pi * f3 * t)

# Step 2: Compute the DFT using numpy's FFT function
N = len(x)
X = np.fft.fft(x)

# Step 3: Compute the frequency axis
frequencies = np.fft.fftfreq(N, T)

# Step 4: Plot the original signal and its frequency spectrum
# Plotting the time-domain signal
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, x)
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# Plotting the frequency spectrum
plt.subplot(2, 1, 2)
plt.plot(frequencies[:N//2], np.abs(X)[:N//2])  # Only plot positive frequencies
plt.title('Frequency Domain Representation (Magnitude)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()

x_reconstructed = np.fft.ifft(X)