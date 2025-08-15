def lfsr(seed, taps, n_bits):
    """
    Linear Feedback Shift Register (LFSR) generator.

    Parameters:
        seed (int): Initial non-zero seed of the LFSR.
        taps (list): List of tap positions (zero-based index).
        n_bits (int): Number of bits to generate.

    Returns:
        list: Generated bit sequence.
    """
    sr = seed
    output = []

    for i in range(n_bits):
        bit = 0
        for t in taps:
            bit ^= (sr >> t) & 1  # XOR the tapped bits
        output_bit = sr & 1
        output.append(output_bit)
        sr = (sr >> 1) | (bit << 7)  # Shift right and insert feedback bit at the left

    return output


# Example usage
seed = 0b0001  # Non-zero seed
taps = [3,1,0]  # Taps for polynomial x^8 + x^6 + x^5 + x^4 + 1
n = 100  # Generate 20 bits

sequence = lfsr(seed, taps, n)
print(sequence)