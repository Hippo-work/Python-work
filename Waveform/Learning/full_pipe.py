import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def generate_data(length):
    return np.random.randint(0,2, length, dtype=np.uint8)

def block_interleave(data,row,cols):
    matrix = np.reshape(data,(rows,cols))
    return matrix.T.flatten()

def hamming74_encode(data):
    G = np.array([
        [1, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1]
    ], dtype=np.uint8)
    
    data = np.reshape(data, (-1, 4))
    encoded = (data @ G) % 2
    return encoded.flatten()

def pad_to_multiple(data, block_size):
    remainder = len(data) % block_size
    if remainder != 0:
        padding = np.zeros(block_size - remainder, dtype=np.uint8)
        data = np.concatenate((data, padding))
    return data

def bpsk_modulate(bits):
    return 2 * bits - 1 # 0 > -1, 1 > +1

### Additive white gaussian noise
def awgn_channel(signal, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    power = np.mean(np.abs(signal)**2)
    noise_power = power / snr_linear
    noise = np.sqrt(noise_power) * np.random.randn(len(signal))
    return signal + noise

def bpsk_demodulate(received):
    return (received >= 0).astype(np.uint8)

def block_deinterleave(data, rows, cols):
    matrix = np.reshape(data, (cols, rows)).T
    return matrix.flatten()

def hamming74_decode(received):
    H = np.array([
        [0, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1]
    ], dtype=np.uint8)
    received = pad_to_multiple(received, 7)  # Just in case
    received = np.reshape(received, (-1, 7))
    decoded = []


    for word in received:
        syndrome = (H @ word) % 2
        syndrome = (syndrome > 0.5).astype(np.uint8)  # Convert to binary
        syndrome_val = int("".join(map(str, syndrome[::-1])), 2)
        
        if syndrome_val != 0:
            word = word.astype(np.uint8)
            word[syndrome_val - 1] ^= 1  # Correct single-bit error
        decoded.append(word[:4])  # Extract original data bits

    return np.array(decoded).flatten()
        



### BER
def calculate_ber(original, recovered):
    errors = np.sum(original != recovered)
    return errors / len(original)


def plot_bitstream(bits, title="Bitstream"):
    bits = np.array(bits).reshape(-1, 1)
    plt.imshow(bits, cmap='Greys', aspect='auto')
    plt.title(title)
    plt.xlabel("Bit")
    plt.ylabel("Index")
    plt.show()

def visualize_bitstream(bits, title="Bitstream"):
    bits = np.array(bits).reshape(-1, 1)  # Column view
    plt.imshow(bits, cmap='Greys', aspect='auto')
    plt.title(title)
    plt.xlabel("Bit")
    plt.ylabel("Index")
    plt.show()

def animate_bitstream(stages, interval=1000):
    fig, ax = plt.subplots()

    def update(i):
        ax.clear()
        ax.imshow(np.array(stages[i]).reshape(-1, 1), cmap='Greys', aspect='auto')
        ax.set_title(f"Stage {i+1}")
        ax.set_xlabel("Bit")
        ax.set_ylabel("Index")

    ani = FuncAnimation(fig, update, frames=len(stages), interval=interval)
    plt.show()


### Parameters
rows, cols = 8, 16
snr_db = 10

### Execute

data = generate_data(rows * cols)


interleaved = block_interleave(data, rows, cols)



encoded_data = hamming74_encode(interleaved)
encoded_data = pad_to_multiple(encoded_data, 7)



modulated = bpsk_modulate(encoded_data)
received = awgn_channel(modulated, snr_db)
demodulated = bpsk_demodulate(received)



decoded_data = hamming74_decode(received)
decoded_data = decoded_data[:len(data)]

deinterleaved = block_deinterleave(decoded_data, rows, cols)
ber = calculate_ber(data, decoded_data)


print(f"Bit Error Rate: {ber:.4f}")

##### Plotting
# visualize_bitstream(data, "Original Data")
# visualize_bitstream(interleaved, "After Interleaving")
# visualize_bitstream(encoded_data, "After FEC Encoding")
# visualize_bitstream(demodulated, "After Demodulation")
# visualize_bitstream(decoded_data, "After FEC Decoding")