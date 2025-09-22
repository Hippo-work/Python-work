import numpy as np
import matplotlib.pyplot as plt


# Step 1: Create a signal with spectral leakage
fs = 500  # Sampling frequency
T = 1/fs  # Sampling period
t = np.arange(0, 1, T)  # Time vector

# Step 1: Create a noisy signal (sum of sinusoids plus noise)
f1 = 100  # Low frequency
f2 = 150  # High frequency
noise = np.random.normal(0, 1.0, len(t))  # Gaussian noise
x_noisy = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t) + noise

# Step 2: Compute the DFT of the noisy signal # convert to power spectrum/freq domain
X_noisy = np.fft.fft(x_noisy)

# Step 3: Design a low-pass filter
low_cutoff_freq = 80  # Set cutoff frequency (Hz)
high_cutoff_freq = 170
frequencies = np.fft.fftfreq(len(t), T)
filter_mask = np.abs(frequencies) < high_cutoff_freq  # Low-pass filter mask

# Step 4: Apply the filter in the frequency domain
X_filtered = X_noisy * filter_mask

# Step 5: Inverse DFT to reconstruct the filtered signal #to time domain right?
x_filtered = np.fft.ifft(X_filtered)

#idft of filter useful?
filter_mask_idft = np.fft.ifft(filter_mask)

# Step 6: Plot the results
plt.figure(figsize=(12, 8))

# Plot the noisy signal and filtered signal
plt.subplot(4, 1, 1)
plt.plot(t, x_noisy, label='Noisy Signal')
plt.title('Noisy Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# plt.subplot(3, 1, 2)
# plt.plot(t, x_filtered, label='Filtered Signal', color='orange')
# plt.title('Filtered Signal (Low-Pass Filter)')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')

plt.subplot(4, 1, 2)
plt.specgram(x_noisy, Fs=fs)
plt.title('Noisy Signal Spectrogram')
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')

# Plot the magnitude spectra of the noisy and filtered signals
plt.subplot(4, 1, 3)
plt.plot(frequencies[:len(t)//2], np.abs(X_noisy)[:len(t)//2], label='Noisy Spectrum')
plt.plot(frequencies[:len(t)//2], np.abs(X_filtered)[:len(t)//2], label='Filtered Spectrum', color='orange')
plt.title('Frequency Domain Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.legend()

# Plot the phase spectrum of the combined signal
plt.subplot(4, 1, 4)
plt.plot(frequencies[:len(t)//2], np.angle(x_noisy)[:len(t)//2], label='Phase Spectrum', color='orange')
plt.title('Phase Spectrum of Combined Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [radians]')
plt.legend()

plt.tight_layout()
plt.show()
