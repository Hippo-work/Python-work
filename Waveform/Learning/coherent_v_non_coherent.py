import numpy as np

Fs = 1000.0            # sample rate (Hz)
N  = 2048              # samples
t  = np.arange(N) / Fs

A   = 1.0              # sinusoid peak amplitude
f0  = 125.0            # test frequency (Hz)

# Try coherent (set f0 = m*Fs/N) vs non-coherent (arbitrary f0)
coherent = True
if coherent:
    m = 256            # integer cycles in N samples
    f0 = m * Fs / N

x = A * np.sin(2*np.pi*f0*t)

# Choose window
win = np.hanning(N)               # Hann window
G   = 0.5                         # Hann coherent gain
xw  = x * win

# FFT (real-input)
X = np.fft.rfft(xw)
freq = np.fft.rfftfreq(N, 1/Fs)

# Amplitude spectrum (single-sided, peak amplitude)
mag = (2.0 / (N * G)) * np.abs(X)   # factor 2 for single-sided (except DC/Nyquist)
mag[0] /= 2.0
if N % 2 == 0:
    mag[-1] /= 2.0                  # Nyquist bin exists when N even

# Find peak and estimate amplitude/frequency
k_peak = np.argmax(mag)
A_est  = mag[k_peak]
f_est  = freq[k_peak]

print(f"Peak at ~{f_est:.3f} Hz, amplitude ~{A_est:.3f} (true A={A})")

import matplotlib.pyplot as plt

plt.figure(figsize=(9,4))
plt.semilogx(freq[1:], 20*np.log10(mag[1:] + 1e-15))  # skip DC for clarity
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dBFS)")
plt.title("Single-sided magnitude spectrum (Hann, amplitude-corrected)")
plt.grid(True, which='both')
plt.show()
