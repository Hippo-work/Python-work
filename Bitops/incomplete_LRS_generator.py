"""
Generate LRS from supplied tap points
input tap points
work with delimiters , and space
check if its ordered weird, reorder numerically
if no 0 at start do i append on or will it be fine
run the function for a list of bits
for a supplied length
initial fill
pack bits to bytes
"""
#2n-1 maximal length


def LRS_generator(taps, length, initial_fill=1):
    #initial fill first bit is default 1 unless supplied

    #init a list for the results
    #need to reverse the list cos thats how the tap points work yeah
    rev_taps = taps[::-1]
    rev_taps.append(0)
    print(rev_taps)
    #after reverse taps
    #make a new list the same length as the highest value in the taps
    # compare lists and output a 1 if they match int values?
    #using inner for
    # if index of taps in the range of the full results is not 0 then make it 1:
    # else make it 0: would this work?
    bin_rev_taps = []
    for t, rev_tap in enumerate(rev_taps):
        if rev_tap != 0:
            bin_rev_taps.append(1)
        else:
            bin_rev_taps.append(0)
    print(bin_rev_taps)
    
    # test = rev_taps[:-(len(rev_taps)-1)]  #gives the first value in a list
    seq_result = []
    if initial_fill != 1:
        for t in rev_taps:
            seq_result.insert(t, 1)
    elif initial_fill == 1:
        seq_result = [initial_fill]
    #pad fill the rest of the array to (length) of 0s
    for i in range(length-1):
        seq_result.append(0)
    print(seq_result)

    #need to read the list from sequence and parse it
    #start example for 4 1 0 (0 3 4)


    i_len = len(taps)
    for i in range(i_len):
        x = 1

    return i_len

"""
need to xor index i, index j and index k..
insert? to index i
increment through for length
"""


if __name__ == "__main__":
    test = LRS_generator([0,2,3], 10)
    print(test)



