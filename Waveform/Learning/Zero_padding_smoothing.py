import numpy as np
import matplotlib.pyplot as plt

''' I don't see much of use in this but maybe this is a bad example'''
# Step 1: Create a signal with spectral leakage
fs = 500  # Sampling frequency
T = 1/fs  # Sampling period
t = np.arange(0, 1, T)  # Time vector
f1 = 50  # Low frequency
f2 = 200  # High frequency

# Step 1: Create a signal (same as before)
noise = np.random.normal(0, 1.0, len(t))  # Gaussian noise
x = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t) + noise

# Step 2: Zero padding (add 100 zeros)
x_padded = np.pad(x, (0, 100), 'constant')

# Step 3: Compute the DFT of the original and padded signal
X = np.fft.fft(x)
X_padded = np.fft.fft(x_padded)

# Step 4: Frequency axis for both
frequencies = np.fft.fftfreq(len(x), T)
frequencies_padded = np.fft.fftfreq(len(x_padded), T)

# Step 5: Plotting the results
plt.figure(figsize=(12, 8))

# Plot the original and padded signals
plt.subplot(3, 1, 1)
plt.plot(t, x, label='Original Signal')
plt.title('Original Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

t_padded = np.arange(0, len(x_padded)*T, T)  # Adjusted time vector for the padded signal
plt.subplot(3, 1, 2)
plt.plot(t_padded, x_padded, label='Zero Padded Signal', color='orange')
plt.title('Zero Padded Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# Plot the frequency spectrum of both
plt.subplot(3, 1, 3)
plt.plot(frequencies[:len(x)//2], np.abs(X)[:len(x)//2], label='Original Spectrum')
plt.plot(frequencies_padded[:len(x_padded)//2], np.abs(X_padded)[:len(x_padded)//2], label='Zero Padded Spectrum', color='orange')
plt.title('Frequency Domain Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')
plt.legend()

plt.tight_layout()
plt.show()
