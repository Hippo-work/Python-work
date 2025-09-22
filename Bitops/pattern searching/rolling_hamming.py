import time
import numpy as np

def bits_to_int(bits):
    x = 0
    for b in bits:
        x = (x << 1) | (1 if b else 0)
    return x

def rolling_hamming_search(text_bits, pattern_bits, max_diff):
    """
    Returns list of start indices where pattern matches within max_diff substitutions.
    """
    n, m = len(text_bits), len(pattern_bits)
    if m == 0 or n < m:
        return []
    pat = bits_to_int(pattern_bits)
    mask = (1 << m) - 1

    # Prime the first window
    w = 0
    res = []
    for i in range(n):
        w = ((w << 1) | (1 if text_bits[i] else 0)) & mask
        if i >= m - 1:
            # window [i-m+1 : i+1]
            if (w ^ pat).bit_count() <= max_diff:
                res.append(i - m + 1)
    return res

# Example
t = np.random.randint(0,2, size=1000000)
p = [0,1,1,1]
start_time = time.time()
rolling_hamming_search(t, p, max_diff=1)  # e.g., indices within 1 bit
rolling_hamming_search(t, p, max_diff=1)
rolling_hamming_search(t, p, max_diff=1)
rolling_hamming_search(t, p, max_diff=1)
rolling_hamming_search(t, p, max_diff=1)
end_time = time.time()
print(end_time - start_time)