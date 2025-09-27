'''Apply Taps'''
from functools import reduce
from operator import ixor
### say if the taps are 0,3,5
### output a 1 for every index position in above, then reverse and swap the last to 0 or leave as?
### so 0,3,5 would be 1,0,0,1,0,1 flipped to 1,0,1,0,0,1

#from user
tap_input = 0,4,5,6,8
# creates the tap array, adds a 1 for the index value in the tap_input
# e.g. 0,3,5 = 1,0,0,1,0,1 (not sure need the first 1, but keep it cos it works correctly)
to_apply_taps = [1 if idx in tap_input else 0 for idx in range(max(tap_input) + 1)]
#reverse the taps because x5+x3+1 taps are 10100
to_apply_taps = to_apply_taps[::-1]
print(to_apply_taps)

# rando data for test
# to_data = np.random.randint(0,2,size=100).tolist()
to_data = [1,0,0,1,0,1,1,0,0,0,1,0,0,1,0,1]

#apply taps function
def apply_taps(input_data:list, taps:list):
    #adds the length of the taps to the end so the window total size = length of data
    data = input_data + taps
    #size of register
    window_size = len(taps)
    #ends up being the length of the data
    window_total = len(data) - (window_size) + 1

    output_array = []
    for i in range(window_total):
        #fill register
        register = data[i:i+window_size]
        # will take the register index if there is a 1 in that index in taps (takes the bits to xor together)
        to_xor = [register[idx] for idx in range(len(taps)) if taps[idx] == 1]
        # reduce is basically a for loop, xor each value in the array together with ixor
        result = reduce(ixor, to_xor)
        # add it to the output array
        output_array.append(result)
    #remove the last value to fit input data length (may be omitted if i remove the +1 from window_total, will need to check whats best)
    output_array.pop(-1)
    return output_array

result_data = apply_taps(to_data, to_apply_taps)
print(result_data)