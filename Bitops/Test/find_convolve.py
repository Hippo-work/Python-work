import numpy as np
import time
start_time = time.time()

# Example input signal
data_in = np.random.randint(0,2,size=1000)
signal = np.array(data_in)

# Target pattern
pattern = np.array([1, 0, 1, 0, 0, 1])

# Flip the pattern for convolution
kernel = pattern[::-1]

# Perform convolution
conv_result = np.convolve(signal, kernel, mode='valid')

# Count of 1s in the pattern (used as match score)
match_score = np.sum(pattern)

# Find indices where the pattern matches
match_indices = np.where(conv_result == match_score)[0]

end_time = time.time()

# print("Convolution result:", conv_result)
print("Pattern found at indices:", match_indices)

print("Time:", end_time - start_time)