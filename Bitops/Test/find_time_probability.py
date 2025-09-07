from math import sqrt
import numpy as np
import time
from scipy.stats import binom
from numba import njit

def print_array_in_lines(arr, per_line=10):
    for i in range(0, len(arr), per_line):
        print(' '.join(str(x) for x in arr[i:i+per_line]))

#try different rando
rng = np.random.default_rng()
data_in = rng.integers(0,2, size= 1000000, dtype=np.uint8)
#inject patterns


# data_in = np.random.randint(0,2,size=10000000)
print(f"data in checks: mean -> {np.mean(data_in)} :: std -> {np.std(data_in)}")

# Example input signal
@njit
def convo(stream, pattern):
    """
    Finds exact matches of a binary pattern in a binary stream using convolution.
    Returns indices where the pattern aligns perfectly.
    """
    
    # print_array_in_lines(stream, 50)
    # print(len(stream))
    # print_array_in_lines(pattern,50)
    pattern_len = len(pattern)
    pattern_sum = np.sum(pattern)

    # Convolve without reversing the pattern
    conv_scores = np.convolve(stream, pattern, mode='valid')

    # Find indices where the score equals the pattern sum
    match_indices = []
    for i, score in enumerate(conv_scores):
        segment = stream[i:i+pattern_len]
        if np.array_equal(segment, pattern):
            match_indices.append(i)

    return match_indices


def theoretical_probability(pattern, p: float = 0.5) -> float:
    """Calculate theoretical probability of a binary pattern assuming i.i.d. Bernoulli trials."""
    theo_prob = 1.0
    for bit in pattern:
        theo_prob *= p if bit == 1 else (1 - p)
    return theo_prob

def z_score(observed, expected_mean, std_dev):
    return (observed - expected_mean) / std_dev
def std_dev(trials,prob_success):
    #trials is the data length - pattern length + 1
    #probability is 1/1024?
    return sqrt(trials * prob_success * (1 - prob_success))


rand_pattern = np.random.randint(0,2,size=20)
pattern = np.array(rand_pattern, dtype=np.uint8)
data_in[500:500+len(pattern)] = pattern
stream = np.array(data_in, dtype=np.uint8)
start_time_1 = time.time()
actual_matches = convo(data_in, pattern)
emp_prob = len(actual_matches) / (len(data_in) - len(pattern) + 1)
theo_prob = theoretical_probability(rand_pattern)
theo_matches = theo_prob * float((len(data_in) - len(pattern) + 1))
expected_count = theo_prob * (len(data_in) - len(pattern) + 1)
z = z_score(len(actual_matches), expected_count, std_dev(len(data_in) - len(pattern) + 1, theo_prob))
end_time_1 = time.time()
print("Pattern found at indices:", actual_matches)
print("Pattern count detected", len(actual_matches))
print("Theoretical counts expected", int(theo_matches))
print("Emp probability", emp_prob)
print("Theoretical probability", theo_prob)
print(f"Emp prob / theo percentages: {(emp_prob / theo_prob) * 100}% difference")
print(f"Z-score:  {z}")


print("Time:", end_time_1 - start_time_1)

### Theoretical
### probability is data length - pattern length + 1 ### which all the possible places for the pattern
### the chance for a random 10 bit pattern is 0.5^10 ### with 0.5 being equally 1 or 0
### amount of matches expected == probability * chance

def matplot():
    import matplotlib.pyplot as plt

    labels = ['Empirical','Theoretical']
    values = [len(actual_matches), theo_matches]

    plt.bar(labels, values, color=['skyblue', 'salmon'])
    plt.ylabel('Occurrences')
    plt.title('Pattern Match Comparison')
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

n = len(data_in) - len(pattern) + 1 # number of trials
p = 0.5 ** len(pattern) # probability of success on each trial 0.5 equal between 1 and 0
k = 5 # number of successes youre asking about "whats the chance of getting exactly 3 heads"

cumulative_prob = 1- binom.cdf(k, n,p)
print(f"Cumulative probability of Pat in data = {cumulative_prob * 100:.6f}%")

#hamming check
'''
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

matches = fuzzy_match(data_in, pattern, max_distance=1)
print("Approximate Hamming matches at indices:", matches)
print("Hamming Count:", len(matches))

def brute_match(stream, pattern):
    matches = []
    for i in range(len(stream) - len(pattern) + 1):
        if np.array_equal(stream[i:i+len(pattern)], pattern):
            matches.append(i)
    return matches
print(f"Brute force:", brute_match(data_in,pattern))
'''