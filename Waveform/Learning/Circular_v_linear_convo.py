import numpy as np

x = np.random.randn(512)
h = np.random.randn(64)

# Linear convolution by zero-padding and FFT
Nlin = len(x) + len(h) - 1
Nfft = 1 << (Nlin - 1).bit_length()   # next power of two
X = np.fft.rfft(np.pad(x, (0, Nfft - len(x))))
H = np.fft.rfft(np.pad(h, (0, Nfft - len(h))))
y = np.fft.irfft(X * H, n=Nfft)[:Nlin]
