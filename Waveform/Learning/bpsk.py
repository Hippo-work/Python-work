import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

'''Parameters of the signal'''
# Parameters
fs = 1000  # Sampling frequency (samples per second)
T = 1/fs   # Sampling period
duration = 100  # Duration of the signal in seconds
f_carrier = 100  # Carrier frequency (Hz)
num_bits = 1000  # Number of bits in the data sequence

# Time vector (for one second of signal)
t = np.arange(0, duration, T)

'''Data'''
# Step 1: Generate a random binary data sequence
data = np.random.randint(0, 2, num_bits)  # Binary data sequence (0 or 1)

'''Empty Array'''
# Step 2: Create a BPSK modulated signal
bpsk_signal = np.zeros(len(t))

'''bits/time'''
# Time vector for each bit
bit_duration = duration / num_bits  # Duration of one bit
'''linspace evenly distributes values between start and stop with step'''
t_bit = np.linspace(0, bit_duration, int(fs * bit_duration), endpoint=False)

'''Generate Signal'''
for i, bit in enumerate(data):
    # Create the carrier for each bit (either 0 or π phase shift)
    phase = 0 if bit == 0 else np.pi  # 0 for bit 0, π for bit 1
    offset = np.pi/4
    carrier = np.cos(2 * np.pi * f_carrier * t_bit + phase) # + offset
    
    # Add the carrier to the BPSK signal at the appropriate time interval
    start_idx = int(i * len(t_bit))
    end_idx = int((i + 1) * len(t_bit))
    bpsk_signal[start_idx:end_idx] = carrier

''' get I & Q and Instantanous Phase(phase domain)'''
# Step 6: Compute the instantaneous phase of the BPSK signal
# Use np.angle to get the phase of the signal
# Analytic signal and instantaneous phase
analytic = hilbert(carrier)
I = np.real(analytic)
Q = np.imag(analytic)
inst_phase = np.angle(analytic)



'''Consellation Plot'''
plt.figure(figsize=(6, 6))
plt.scatter(I, Q, alpha=0.3, color='blue')
plt.title("BPSK Constellation Diagram")
plt.xlabel("In-phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid(True)
plt.axis('equal')
plt.scatter([1, -1], [0, 0], color='red', marker='x', s=100, label='Ideal Symbols')
plt.legend()
plt.show()

'''create plot'''
# Step 3: Plot the BPSK signal in the time domain
plt.figure(figsize=(12, 8))

'''Time Domain of BPSK'''
# Time-domain plot of the BPSK signal
plt.subplot(3, 1, 1)
plt.plot(t, bpsk_signal)
plt.title('BPSK Modulated Signal (Time Domain)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')



# Step 4: Compute the DFT of the BPSK signal
X_bpsk = np.fft.fft(bpsk_signal)
frequencies = np.fft.fftfreq(len(t), T)

print("Generated Data (BPSK):", data)

# Step 5: Plot the frequency domain spectrum (magnitude)
plt.subplot(3, 1, 2)
plt.plot(frequencies[:len(t)//2], np.abs(X_bpsk)[:len(t)//2])
plt.title('BPSK Signal Spectrum (Magnitude)')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude')


# Step 6: Plot the phase of the BPSK signal
plt.subplot(3, 1, 3)
plt.plot(t, inst_phase)
plt.title('Phase Spectrum of BPSK Signal')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [radians]')

plt.tight_layout()
plt.show()

# Output the data sequence for reference

