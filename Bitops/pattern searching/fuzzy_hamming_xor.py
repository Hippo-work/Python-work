import numpy as np
import time
from numba import njit
# @njit
def hamming_search(data, pattern, max_diff):
    data = np.array(data, dtype=np.uint8)
    pat = np.array(pattern, dtype=np.uint8)
    m = len(pat)
    matches = []
    for i in range(len(data) - m + 1):
        diff = np.count_nonzero(data[i:i+m] != pat)
        if diff <= max_diff:
            matches.append(i)
    return matches

data = np.random.randint(0,2, size=1000000)
pattern = [0,1,1,1]
start_time = time.time()
hamming_search(data, pattern, max_diff=1)
hamming_search(data, pattern, max_diff=1)
hamming_search(data, pattern, max_diff=1)
hamming_search(data, pattern, max_diff=1)
hamming_search(data, pattern, max_diff=1)
end_time = time.time()
print(end_time - start_time)