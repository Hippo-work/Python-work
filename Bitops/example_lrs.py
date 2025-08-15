import numpy as np
import matplotlib.pyplot as plt


def lfsr(seed, taps, reg_size=8):
    sr = seed
    while True:
        feedback = 0
        for t in taps:
            feedback ^= (sr >> t) & 1
        output = sr & 1
        sr = (sr >> 1) | (feedback << (reg_size - 1))
        yield output

def geffe_generator(s1_seed, s2_seed, s3_seed, taps1, taps2, taps3, n_bits):
    lfsr1 = lfsr(s1_seed, taps1)
    lfsr2 = lfsr(s2_seed, taps2)
    lfsr3 = lfsr(s3_seed, taps3)
    output = []

    for _ in range(n_bits):
        x = next(lfsr1)
        y = next(lfsr2)
        s = next(lfsr3)
        # Geffe combining function: (s AND x) XOR ((NOT s) AND y)
        z = (s & x) ^ ((~s & 1) & y)
        output.append(z)

    return output

# Seeds and taps for 8-bit LFSRs
s1 = 0b10110110
s2 = 0b11001001
s3 = 0b11100011

t1 = [7, 5, 4, 3]
t2 = [7, 6, 5, 1]
t3 = [7, 3]

out = geffe_generator(s1, s2, s3, t1, t2, t3, 64)
print("Geffe output:", out)

def plot_lfsr_bits(bitstream, title="LFSR Output"):
    plt.figure(figsize=(12, 2))
    plt.plot(bitstream, drawstyle='steps-mid')
    plt.title(title)
    plt.xlabel("Bit Index")
    plt.ylabel("Bit Value")
    plt.grid(True)
    plt.ylim(-0.2, 1.2)
    plt.show()

plot_lfsr_bits(out, title="Geffe Generator Output")

def show_lfsr_image(bitstream, width):
    import numpy as np

    height = len(bitstream) // width
    bit_array = np.array(bitstream[:height * width], dtype=np.uint8).reshape((height, width))

    plt.figure(figsize=(6, 6))
    plt.imshow(bit_array, cmap='gray', interpolation='nearest')
    plt.title("LFSR Output as Image")
    # plt.axis('off')
    plt.show()

show_lfsr_image(out, width=16)