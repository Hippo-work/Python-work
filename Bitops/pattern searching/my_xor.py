import numpy as np
import time
from numba import njit

@njit
def bitwise_find(data, norm_pattern,threshold=0):
    pattern_len = len(norm_pattern)
    matches = []
    window_total = len(data) - pattern_len + 1

    for i in range(window_total):
        segment = data[i:i+pattern_len]
        xor = np.bitwise_xor(segment, norm_pattern)
        score = np.sum(xor)  # or use np.count_nonzero(xor) for Hamming distance
        if score <= threshold:
            matches.append(i)
    return matches

data = np.array(np.random.randint(0,2, size=1000000))
pattern = np.array([0,1,1,1])
start_time = time.time()
bitwise_find(data, pattern, threshold=1)
bitwise_find(data, pattern, threshold=1)
bitwise_find(data, pattern, threshold=1)
bitwise_find(data, pattern, threshold=1)
bitwise_find(data, pattern, threshold=1)
end_time = time.time()
print(end_time - start_time)