import numpy as np
import matplotlib.pyplot as plt

# Parameters
fs = 1000  # Sampling frequency (samples per second)
T = 1/fs   # Sampling period
duration = 1  # Duration of the signal in seconds
f_carrier = 100  # Carrier frequency (Hz)
num_bits = 10  # Number of bits in the data sequence

# Time vector (for one second of signal)
t = np.arange(0, duration, T)

# Step 1: Generate a random binary data sequence
data = np.random.randint(0, 2, num_bits)  # Binary data sequence (0 or 1)

# Step 2: Create a BPSK modulated signal
bpsk_signal = np.zeros(len(t))

# Time vector for each bit
bit_duration = duration / num_bits  # Duration of one bit
t_bit = np.linspace(0, bit_duration, int(fs * bit_duration), endpoint=False)

for i, bit in enumerate(data):
    # Create the carrier for each bit (either 0 or π phase shift)
    phase = 0 if bit == 0 else np.pi  # 0 for bit 0, π for bit 1
    carrier = np.cos(2 * np.pi * f_carrier * t_bit + phase)
    
    # Add the carrier to the BPSK signal at the appropriate time interval
    start_idx = int(i * len(t_bit))
    end_idx = int((i + 1) * len(t_bit))
    bpsk_signal[start_idx:end_idx] = carrier

# Step 3: Compute the instantaneous phase of the BPSK signal
# Use np.angle to get the phase of the signal
instantaneous_phase = np.angle(np.exp(1j * (2 * np.pi * f_carrier * t + np.pi * (data.repeat(len(t_bit) // num_bits)))))

# Step 4: Plot the time-domain phase
plt.figure(figsize=(10, 6))

plt.plot(t, instantaneous_phase)
plt.title('Time-Domain Phase of BPSK Signal')
plt.xlabel('Time [s]')
plt.ylabel('Phase [radians]')
plt.grid(True)
plt.show()

# Output the data sequence for reference
print("Generated Data (BPSK):", data)
