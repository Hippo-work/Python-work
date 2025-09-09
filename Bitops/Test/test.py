import numpy as np

def define_patterns(pattern):
    normal_pattern = np.array(pattern, dtype="uint8")
    inverted_pattern = np.array(1 - normal_pattern, dtype="uint8")
    reverse_eight_pattern = []
    for i in range(0, len(pattern), 8):
        byte = pattern[i:i+8]
        reversed_byte = byte[::-1]
        reverse_eight_pattern.extend(reversed_byte)
    reverse_eight_pattern = np.array(reverse_eight_pattern, dtype="uint8")

    delta_pattern = []
    for i in range(0, len(pattern)):
        delta = pattern[i] ^ pattern[i -1]
        delta_pattern.append(delta)
    delta_pattern.pop(0)  # Remove the first element as it has no previous bit to compare
    delta_pattern = np.array(delta_pattern, dtype="uint8")

    return normal_pattern, inverted_pattern, reverse_eight_pattern, delta_pattern

test_n, test_i, test_r8, deltas= define_patterns([1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0])  # Example usage
print(test_n)
print(test_i)
print(test_r8)
print(deltas)