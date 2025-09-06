import numpy as np

def hamming_distance(a, b):
    """Compute Hamming distance between two binary arrays."""
    return np.sum(np.array(a) != np.array(b))

def fuzzy_match(data, pattern, max_distance=1):
    """Find indices where pattern approximately matches data within max_distance."""
    signal = np.array(data)
    pattern = np.array(pattern)
    k = len(pattern)
    match_indices = []

    for i in range(len(signal) - k + 1):
        window = signal[i:i+k]
        dist = hamming_distance(window, pattern)
        if dist <= max_distance:
            match_indices.append(i)

    return match_indices

data = [1, 0, 1, 1, 0, 1, 0, 1]
pattern = [1, 0, 1]
matches = fuzzy_match(data, pattern, max_distance=1)
print("Approximate matches at indices:", matches)