def bits_to_int(bits):
    return int(''.join(map(str, bits)), 2)

def bit_hamming_search(data_bits, pattern_bits, max_diff):
    m = len(pattern_bits)
    pat_int = bits_to_int(pattern_bits)
    matches = []
    for i in range(len(data_bits) - m + 1):
        window_int = bits_to_int(data_bits[i:i+m])
        if (window_int ^ pat_int).bit_count() <= max_diff:
            matches.append(i)
    return matches