class LFSR:
    def __init__(self, seed=0b11111111, taps=[7,6,4,1], width=8):
        self.state = seed
        self.taps = taps
        self.width = width

    def step(self):
        # XOR the tapped bits
        feedback = 0
        for t in self.taps:
            feedback ^= (self.state >> t) & 1

        # Shift left and insert feedback bit
        self.state = ((self.state << 1) & ((1 << self.width) - 1)) | feedback

        return self.state

    def get_bit(self):
        return self.state & 1

    def get_state(self):
        return self.state

def pseudo_randomize(data: bytes, lfsr: LFSR) -> bytes:
    randomized = bytearray()

    for byte in data:
        rand_byte = 0
        for i in range(8):
            lfsr_bit = lfsr.step() & 1
            bit = ((byte >> i) & 1) ^ lfsr_bit
            rand_byte |= (bit << i)
        randomized.append(rand_byte)

    return bytes(randomized)

if __name__ == "__main__":
    data = b"Hello World"  # Original data

    # Initialize LFSR with a seed
    lfsr = LFSR(seed=0b10101010)

    # Randomize
    encrypted = pseudo_randomize(data, lfsr)
    print("Encrypted:", encrypted)

    # Reset LFSR to same seed to decrypt
    lfsr = LFSR(seed=0b10101010)
    decrypted = pseudo_randomize(encrypted, lfsr)
    print("Decrypted:", decrypted)
