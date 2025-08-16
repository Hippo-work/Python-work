import matplotlib.pyplot as plt

# Example: 4-bit maximal length LFSR
def lfsr(seed:list, taps:list, length:int):
    sr = seed.copy()
    output = []
    for _ in range(length):
        feedback = 0
        for t in taps:
            feedback ^= sr[t]
        output.append(sr[-1])
        sr = [feedback] + sr[:-1]
    return output

seed = [1, 0]#seed length must = tap length #also must be binary to work
taps = [0,1]  # x^4 + x + 1 ## seems the 0 tap is ommitted automatically
length = (2**5 - 1) * 2

sequence = lfsr(seed, taps, length)
print(sequence)
print(max(seed)) #gets the max int value in a list
#need to modify it so that if no seed is input, it defaults to [1,0*(max(taps))]

test_len = [0 for t in len(max(taps))]
print(test_len)