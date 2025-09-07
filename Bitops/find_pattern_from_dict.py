import time
import numpy as np
from numba import njit
import json
from statistics import median
from multiprocessing import Pool, cpu_count

def load_patterns(file_patterns="Bitops/dict_pattern.json", file_fw="Bitops/dict_fw.json"):
    with open(file_patterns, "r") as f_in:
        pattern_dict =  json.load(f_in)
    with open(file_fw, "r") as f_in:
        fw_dict = json.load(f_in)
    return pattern_dict, fw_dict

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
        if np.array_equal(segment, pattern): # full match
            match_indices.append(i)
        elif np.array_equal(segment, 1 - pattern): #flipped compliment (inverted)
            match_indices.append(i)
    return match_indices

def find_pattern_worker(args):
    data, dicto, arrays, verbose = args
    found = {}
    if verbose:
        print(f"Searching for {dicto}")
    for array in arrays:
        extracted_pattern = [int(bit) for bit in array]
        pattern_np = np.array(extracted_pattern)
        find_pat = convolute_pattern(data, pattern_np)
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

def find_pattern(data, pattern_dict, verbose: bool=False):
    found = {}
    args_list = [(data, dicto, arrays, verbose) for dicto, arrays in pattern_dict.items()]
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
    #actual match ount, theoretical probability, length of data - length of pattern +1
    expected_count = expected_prob * total_trials
    std_dev = np.sqrt(expected_prob * (1 - expected_prob) * total_trials)
    return (observed_count - expected_count) / std_dev

def probability(found_dict, fw_dict, length_of_data:int, verbose: bool= False):
    low_probability_result = []
    high_probability_result = []
    very_high_probability_result = []
    winner_result = []
    for key, values in found_dict.items():
        for v in range(len(values)):
            FW_guess = 0
            pattern = values[v]["pattern"]                  #array of pattern that matched
            length_of_pattern = len(values[v]["pattern"])   #length of pattern
            actual_match_count = int(values[v]["count"])    #how many times it matched
            to_deltas = values[v]["matches"]                #the index where it matched
            if len(to_deltas) > 1:                
                    deltas = np.diff(to_deltas)
                    FW_guess = int(median(deltas))
            total_windows = length_of_data - length_of_pattern + 1
            emp_prob = (actual_match_count / total_windows)
            theo_prob = theoretical_probability(pattern)
            z_score = z_score_count(actual_match_count, theo_prob, total_windows)
            if verbose:
                print(key)
                print("     Frame Width guess:          ", int(FW_guess)) #the deltas between the indices  
                print("     Pattern Found Count:        ", actual_match_count)
                print("     Random Data expected Count: ", int(theo_prob * length_of_data))
                print("     Z-score:                    ", z_score)
                print("     Database FW Options:         ", fw_dict.get(key, []))
            if z_score >= 5.0 or z_score <= -5.0:
                loop_break = False
                if z_score >= 50.0 or z_score <= -50.0:
                    if FW_guess > 0:
                        for fw in fw_dict.get(key, []):
                            if FW_guess and abs(FW_guess - fw) / fw <= 0.1: #within 10%
                                FW_guess = fw
                                winner_result.append([key,"FW guess: "+str(FW_guess if FW_guess else 0),"Match count: "+str(actual_match_count),"Z-Score: " + str(z_score),"Match Locations: "+ str(to_deltas)])
                                loop_break = True
                                break
                        else:
                            very_high_probability_result.append([key,"FW guess: "+str(FW_guess if FW_guess else 0),"Match count: "+str(actual_match_count),"Z-Score: " + str(z_score),"Match Locations: "+ str(to_deltas)])
                            loop_break = True
                    else:
                        very_high_probability_result.append([key,"FW guess: "+str(FW_guess if FW_guess else 0),"Match count: "+str(actual_match_count),"Z-Score: " + str(z_score),"Match Locations: "+ str(to_deltas)])
                        loop_break = True
                if loop_break:
                    break
                else:
                    high_probability_result.append([key,"FW guess: "+str(FW_guess if FW_guess else 0),"Match count: "+str(actual_match_count),"Z-Score: " + str(z_score),"Match Locations: "+ str(to_deltas)])
                    break
            else:
                low_probability_result.append([key, "Match count: "+str(actual_match_count)])
    return low_probability_result, high_probability_result, very_high_probability_result, winner_result

def runner(data_in,log=False, verbose=False):
    data_in = data_in[:50000] #trim data for speed
    found_dict = find_pattern(data_in,pattern_dict, verbose) #search for patterns, save as dict
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
    low_prob, high_prob, very_high_prob, winner_prob = runner(data_in, log=True, verbose=False)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")

    if low_prob:
        print(f"\nLow Probability matches: {[match[0] for match in low_prob[:5]]}\n...compressed list. Check find.log for more\n")
    if high_prob:
        print(f"\nMaybe Probability matches: {[match[0] for match in high_prob[:10]]}\n...compressed list. Check find.log for more details\n")
    if very_high_prob:
        print("\n")
        for item in very_high_prob:
            print(f"Very High Probability match!: {item}")
    if winner_prob:
        print("\n")
        for item in winner_prob:
            print(f"We have a winner!: {item}")
    print("\nFinished\n")