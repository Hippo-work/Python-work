from functools import lru_cache
import time
import numpy as np
from numba import njit
import json
from statistics import median
from multiprocessing import Pool, cpu_count
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests
import gc
import asyncio

# @lru_cache(maxsize=4096)
def load_patterns(file_patterns="Bitops/dict_pattern.json", file_fw="Bitops/dict_fw.json"):
    with open(file_patterns, "r") as f_in:
        pattern_dict =  json.load(f_in)
    with open(file_fw, "r") as f_in:
        fw_dict = json.load(f_in)
    return pattern_dict, fw_dict
# @lru_cache(maxsize=4096)
def load_data(file_path, size=50000):
    ### filepath here
    # with open(file_path, "rb") as f_in:
    #     data_in = f_in.read(size)
    data_in = np.random.randint(0,2,size)
    #inject a pattern with FW of 100
    data_in[0:43] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
    # data_in[100:143] = [1,0,1,1,1,1,1,1,0,0,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0]
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
    return data_in

@njit
def sliding_window_pattern(data, pattern):
    pattern_len = len(pattern)
    pattern_sum = np.sum(pattern)
    threshold = 0.9
    match_indices = []
    for i, j in enumerate(data):
        segment = data[i:i+pattern_len]
        segment_sum = np.sum(segment)
        if np.array_equal(segment, pattern): # full match
            match_indices.append(i)
        elif np.array_equal(segment, 1 - pattern): #flipped compliment (inverted)
            match_indices.append(i)
    return match_indices

@njit
def sliding_window_hamming(data, pattern, max_mismatches=1):
    pattern_len = len(pattern)
    match_indices = []
    for i in range(len(data) - pattern_len + 1):
        segment = data[i:i+pattern_len]
        mismatches = np.sum(segment != pattern)
        if mismatches <= max_mismatches:
            match_indices.append(i)
    return match_indices

def define_patterns(pattern):
    normal_pattern = np.array(pattern, dtype="uint8")
    inverted_pattern = np.array(1 - normal_pattern, dtype="uint8")
    reverse_eight_pattern = []
    for i in range(0, len(pattern), 8):
        byte = pattern[i:i+8]
        reversed_byte = byte[::-1]
        reverse_eight_pattern.extend(reversed_byte)
    reverse_eight_pattern = np.array(reverse_eight_pattern, dtype="uint8")
    return normal_pattern, inverted_pattern, reverse_eight_pattern

@njit
def bitwise_find(data, norm_pattern, inv_pattern, r8_pattern, threshold=0):
    pattern_len = len(norm_pattern)
    matches = []
    window_total = len(data) - pattern_len + 1

    for i in range(window_total):
        segment = data[i:i+pattern_len]
        xor = np.bitwise_xor(segment, norm_pattern)
        xor_invert = np.bitwise_xor(segment, inv_pattern)
        xor_r8 = np.bitwise_xor(segment, r8_pattern)
        score = np.sum(xor)  # or use np.count_nonzero(xor) for Hamming distance
        score_invert = np.sum(xor_invert)
        score_r8 = np.sum(xor_r8)
        score = min(score, score_invert, score_r8)
        if score <= threshold:
            matches.append(i)
    return matches

def find_pattern_worker(args):
    data, dicto, arrays, threshold, verbose = args
    found = {}
    if verbose:
        print(f"Searching for {dicto}")
    for array in arrays:
        extracted_pattern = [int(bit) for bit in array]
        pattern_np, inv_pattern_np, r8_pattern_np = define_patterns(extracted_pattern)
        find_pat = bitwise_find(data, pattern_np, inv_pattern_np, r8_pattern_np, threshold)
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
    return found

def find_pattern(data, pattern_dict, threshold, verbose: bool=False):
    found = {}
    args_list = [(data, dicto, arrays, threshold, verbose) for dicto, arrays in pattern_dict.items()]
    with Pool(cpu_count() -1) as pool:
        results = pool.map(find_pattern_worker, args_list)
    for result in results:
        for dicto, matches in result.items():
            if dicto not in found:
                found[dicto] = []
            found[dicto].extend(matches)
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
    expected_count = expected_prob * total_trials
    std_dev = np.sqrt(expected_prob * (1 - expected_prob) * total_trials)
    if std_dev == 0:
        return 0
    return (observed_count - expected_count) / std_dev

def p_value_from_z(z):
    # Two-sided p-value from  z-score
    return 2 * (1 - norm .cdf(abs(z)))

def probability (found_dict, fw_dict, length_of_data:int, verbose: bool= False):
    low_probability_result = []
    high_probability_result = []
    very_high_probability_result = []
    winner_result = []
    p_values = []
    all_results = []

    # First pass: collect all  z-scores and p-values
    for key,  values in found_dict.items():
        for v  in range(len(values)):
            FW_guess = 0
            pattern = values[v]["pattern"]
            length_of_pattern = len(values[v]["pattern"])
            actual_match_count = int(values[v]["count"])
            to_deltas = values[v]["matches"]
            if len(to_deltas) > 1:
                deltas = np.diff(to_deltas)
                FW_guess = int(median(deltas))
            total_windows = length_of_data - length_of_pattern + 1
            emp_prob = (actual_match_count / total_windows)
            theo_prob = theoretical_probability(pattern)
            z_score = z_score_count(actual_match_count, theo_prob, total_windows)
            p_val = p_value_from_z(z_score)
            p_values.append(p_val)
            all_results.append((key, values[v], FW_guess, z_score, p_val, to_deltas))

    # Multiple hypothesis correction (Benjamini-Hochberg FDR)
    reject, pvals_corrected, _, _ = multipletests(p_values, alpha=0.001, method='fdr_bh')

    # Second pass: assign results based on corrected p-values
    for idx, (key, value, FW_guess, z_score, p_val, to_deltas) in enumerate(all_results):
        pval_corr = pvals_corrected[idx]
        if verbose:
            print(key)
            print("     Frame Width guess:          ", int(FW_guess))
            print("     Pattern Found Count:        ", int(value["count"]))
            print("     Random Data expected Count: ", int(theoretical_probability(value["pattern"]) * length_of_data))
            print("      Z-score:                    ", z_score)
            print("      p-value (raw):              ", p_val) 
            print("     p-value (corrected):        ", pval_corr)
            print("     Database FW Options:        ", fw_dict.get(key, []))
        
        # Normalize FW_guess if it's close to any fw in fw_dict[key]
        matched_fw = None
        if FW_guess > 0:
            for fw in fw_dict.get(key, []):
                if abs(FW_guess - fw) / fw <= 0.1:
                    matched_fw = fw
                    break

        # Assign to appropriate result bucket
        if matched_fw is not None and abs(z_score) > 10000.0:
            winner_result.append([
                key,
                f" FW matched!!: {matched_fw}",
                f" Match count: {value['count']}",
                f" Z-Score: {z_score}",
                f" Match Locations: {to_deltas}"
            ])
        elif abs(z_score) > 100000.0:
            very_high_probability_result.append([
                key,
                f" FW guess: {FW_guess if FW_guess else 0}",
                f" Match count: {value['count']}",
                f" Z-Score!!: {z_score}",
                f" Match Locations: {to_deltas}"
            ])
        elif abs(z_score) > 1000.0:  # You can adjust this threshold if needed
            high_probability_result.append([
                key,
                f" FW guess: {FW_guess if FW_guess else 0}",
                f" Match count: {value['count']}",
                f" Z-Score: {z_score}",
                f" Match Locations: {to_deltas}"
            ])
        # else:
        #     low_probability_result.append([
        #         key,
        #         f" Match count: {value['count']}",
        #     ] )
    return low_probability_result, high_probability_result, very_high_probability_result, winner_result

def runner(data_in,log=False, threshold=0, verbose=False):
    data_in = data_in[:50000] #trim data for speed
    found_dict = find_pattern(data_in,pattern_dict, threshold, verbose) #search for patterns, save as dict
    gc.collect() #garbage collect to free memory
    low_prob, high_prob, very_high_prob, winner_prob = probability(found_dict, fw_dict, len(data_in), verbose) #prob analysis
    if log: #output log file
        with open("Bitops/Test/find.log", "w") as f_out:
            f_out.write("-- Likely Exact Probability Matches --\n")
            for item in winner_prob:
                f_out.write(f"  - {item}\n")

            f_out.write("-- Very High Probability Matches --\n")
            for item in very_high_prob:
                f_out.write(f"  - {item}\n")

            f_out.write("\n\n-- High Probability Matches --\n")
            for item in high_prob:
                f_out.write(f"  - {item}\n")

            f_out.write("\n\n-- Low Probability Matches --\n")
            for item in low_prob:
                f_out.write(f"  - {item}\n")
    return low_prob, high_prob, very_high_prob, winner_prob

if __name__ == "__main__":
    print("\nStarting pattern search...")
    start_time = time.time()
    pattern_dict, fw_dict = load_patterns() #load patterns from json
    data_in = load_data(None,size=10000) #load data from binary file
    low_prob, high_prob, very_high_prob, winner_prob = runner(data_in, log=True, threshold=1, verbose=False)
    
    if low_prob:
        print(f"\nLow Probability matches: {[match[0] for match in low_prob[:5]]}\n...compressed list. Check find.log for more\n")
    if high_prob:
        print(f"\nMaybe Probability matches: {[match[0] for match in high_prob[:10]]}\n...compressed list. Check find.log for more details\n")
    if very_high_prob:
        print("\n")
        for item in very_high_prob:
            print(f"Very High Probability match!: {item[0] + item [1] + item[2] + item[3]}")
    if winner_prob:
        print("\n")
        for item in winner_prob:
            print(f"We have a winner!: {item[0] + item [1] + item[2] + item[3]}")
    print("\nFinished\n")
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")