import numpy as np
import time
import asyncio
import json




def bits_to_int(bits):
    x = 0
    for b in bits:
        x = (x << 1) | (1 if b else 0)
    return x


def multi_pattern_hamming(text_bits, patterns, max_diff):
    """
    patterns: dict[name] = list[int] bits
    max_diffs: dict[name] = int (allowed substitutions)
    Returns dict[name] = list of start indices
    """
    # Group patterns by length
    by_len = {}
    for name, pat_bits in patterns.items():
        m = len(pat_bits)
        by_len.setdefault(m, []).append(name)

    results = {name: [] for name in patterns}
    n = len(text_bits)

    for m, names in by_len.items():
        if m == 0 or n < m:
            continue

        mask = (1 << m) - 1
        # Precompute packed patterns per name
        pat_ints = {name: bits_to_int(patterns[name]) for name in names}

        # Rolling window for this length
        w = 0
        for i in range(n):
            w = ((w << 1) | (1 if text_bits[i] else 0)) & mask
            if i >= m - 1:
                start = i - m + 1
                # Check all patterns of this length at this start
                for name in names:
                    if (w ^ pat_ints[name]).bit_count() <= max_diff:
                        results[name].append(start)

    return results

# Example
data = np.random.randint(0,2, size=1000000)
patterns = {
    "p0": [0,1,1,1],
    "p1": [0,1,1,1,0],
    "p2": [0,1,1,1,0,0],
    "p3": [0,1,1,1,0,1,0],
    "p4": [0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1],
}
# max_diffs = {"p0": 0, "p1": 0, "p2":0, "p3":0, "p4":0}
start_time = time.time()
multi_pattern_hamming(data, patterns, max_diff=0)
end_time = time.time()
print(end_time - start_time)