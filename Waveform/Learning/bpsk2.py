import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt

# Parameters
Fs = 1000       # Sampling frequency
fc = 100        # Carrier frequency
N = 1000        # Number of samples
t = np.arange(N) / Fs

# Generate random BPSK bits
bits = np.random.randint(0, 2, N)
phase = np.pi * (1 - bits)  # 0 for bit=1, π for bit=0

# BPSK signal
carrier = np.cos(2 * np.pi * fc * t + phase)
signal = carrier

# Analytic signal and instantaneous phase
analytic = hilbert(signal)
inst_phase = np.unwrap(np.angle(analytic))

# Plot
plt.figure(figsize=(10, 4))
plt.plot(t, inst_phase)
plt.title("Instantaneous Phase of BPSK Signal")
plt.xlabel("Time (s)")
plt.ylabel("Phase (radians)")
plt.grid(True)
plt.show()