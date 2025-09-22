import numpy as np
from scipy.signal import fftconvolve
import time
start_time = time.time()

# Input signal
data_in = np.random.randint(0,2,size=1000)
signal = np.array(data_in)
pattern = np.array([1, 0, 1, 0, 0, 1])

def fft_convolve(signal, pattern):
    # Target pattern
    

    # Flip the pattern for convolution
    kernel = pattern[::-1]

    # Perform FFT-based convolution
    conv_result = fftconvolve(signal, kernel, mode='valid')

    # Match score (number of 1s in the pattern)
    match_score = np.sum(pattern)

    # Find perfect matches
    match_indices = np.where(np.isclose(conv_result, match_score))[0]

    return match_indices


match_indices = fft_convolve(signal, pattern)

end_time = time.time()

# print("FFT Convolution result:", conv_result)
print("Pattern found at indices:", match_indices)
print("Time:", end_time - start_time)