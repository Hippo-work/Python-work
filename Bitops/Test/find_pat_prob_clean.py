import time
import numpy as np
from numba import njit
import json
from statistics import median

with open("Bitops/binary_dict.json", "r") as f_in:
    pattern_dict = json.load(f_in)

data_in = np.random.randint(0,2,size=100000)
#inject a pattern with FW of 100
data_in[0:43] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
data_in[100:143] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
data_in[200:243] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
data_in[300:343] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
data_in[400:443] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
data_in[500:543] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0] 
data_in[600:643] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0] 
data_in[700:743] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0] 
data_in[800:843] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0] 
data_in[900:943] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0] 
#second pattern with a FW of 500
data_in[50:92] = [1,0,1,0,1,1,1,1,0,0,0,1,0,1,1,1,0,0,0,1,0,0,1,1,0,1,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1]
data_in[550:592] = [1,0,1,0,1,1,1,1,0,0,0,1,0,1,1,1,0,0,0,1,0,0,1,1,0,1,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1]


@njit
def convolute_pattern(data, pattern):
    """
    Finds exact matches of a binary pattern in a binary stream using convolution.
    Returns indices where the pattern aligns perfectly.
    """
    pattern_len = len(pattern)
    pattern_sum = np.sum(pattern)
    # Convolve without reversing the pattern
    conv_scores = np.convolve(data, pattern, mode='valid')
    # Find indices where the score equals the pattern sum
    match_indices = []
    for i, score in enumerate(conv_scores):
        segment = data[i:i+pattern_len]
        if np.array_equal(segment, pattern):
            match_indices.append(i)
    return match_indices

def find_pattern(data, pattern_dict, verbose: bool=False):
    found = {}
    for dicto, arrays in pattern_dict.items():
        if verbose:
            print(f"Searching for {dicto}")
        for array in arrays:
            extracted_pattern = []
            for bit in array:
                extracted_pattern.append(int(bit))
            pattern_np = np.array(extracted_pattern)
            find_pat = convolute_pattern(data,pattern_np)
            if find_pat:
                count = len(find_pat)
                if verbose:
                    print(f"Pattern found for: {dicto} -- Count: {count} -- Pattern:{pattern_np[:20]}")
                if dicto not in found:
                    found[dicto] = []
                found[dicto].append({
                    "pattern": extracted_pattern,
                    "count": count,
                    "matches": find_pat
                })
    if found:
        return found
    else:
        print("No patterns found")
        return 
@njit
def theoretical_probability(pattern, p: float = 0.5) -> float:
    """Calculate theoretical probability of a binary pattern assuming i.i.d. Bernoulli trials."""
    theo_prob = 1.0
    for bit in pattern:
        theo_prob *= p if bit == 1 else (1 - p)
    return theo_prob

def z_score_count(observed_count, expected_prob, total_trials):
    #actual match ount, theoretical probability, length of data - length of pattern +1
    expected_count = expected_prob * total_trials
    std_dev = np.sqrt(expected_prob * (1 - expected_prob) * total_trials)
    return (observed_count - expected_count) / std_dev

def probability(found_dict, length_of_data:int):
    low_probability_result = []
    high_probability_result = []
    very_high_probability_result = []
    for key, values in found_dict.items():
        for v in range(len(values)):
            print(key)                                      # key, e.g Dict1
            pattern = values[v]["pattern"]                  #array of pattern that matched
            length_of_pattern = len(values[v]["pattern"])   #length of pattern
            actual_match_count = int(values[v]["count"])    #how many times it matched
            to_deltas = values[v]["matches"]
            if len(to_deltas) > 1:                #the index where it matched
                deltas = np.diff(to_deltas)
                FW_guess = median(deltas)
                print("     Frame Width guess:          ", int(FW_guess))                     #the deltas between the indices    
            total_windows = length_of_data - length_of_pattern + 1
            emp_prob = (actual_match_count / total_windows)
            theo_prob = theoretical_probability(pattern)
            z = z_score_count(actual_match_count, theo_prob, total_windows)
            print("     Pattern Found Count:        ", actual_match_count)
            print("     Random Data expected Count: ", int(theo_prob * length_of_data))
            print("     Z-score:                    ", z)
            if -5.0 > z > 5.0:
                if -50.0 > z > 50.0:
                    very_high_probability_result.append(key)
                else:
                    high_probability_result.append(key)
            else:
                low_probability_result.append(key)
    return low_probability_result, high_probability_result, very_high_probability_result


def runner(log=False, verbose=False):
    found_dict = find_pattern(data_in,pattern_dict, verbose)
    low_prob, high_prob, very_high_prob = probability(found_dict, len(data_in))
    if log:
        with open("Bitops/Test/find.log", "w") as f_out:
            f_out.write(f"--Very High probability matches-- {very_high_prob}\n\n--High probability matches-- {high_prob}\n\n--Low probability matches-- {low_prob}")
    return low_prob, high_prob, very_high_prob

start_time = time.time()
low_prob, high_prob, very_high_prob = runner(log=False, verbose=False)
end_time = time.time()
print(f"Time taken: {end_time - start_time}")


if low_prob:
    print(f"\nLow Probability matches: {low_prob[:10]}... check log for more\n")
if high_prob:
    print(f"\nHigh Probability matches: {high_prob}\n")
if very_high_prob:
    print(f"\nVery High Probability matches!: {very_high_prob}\n")