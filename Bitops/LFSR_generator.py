from functools import reduce
from operator import ixor

tap_input = 0,4,5,6,8
# creates the tap array, adds a 1 for the index value in the tap_input
# e.g. 0,3,5 = 1,0,0,1,0,1 (not sure need the first 1, but keep it cos it works correctly)
to_apply_taps = [1 if idx in tap_input else 0 for idx in range(max(tap_input) + 1)]
#reverse the taps because x5+x3+1 taps are 10100
to_apply_taps = to_apply_taps[::-1]
to_apply_taps.pop(-1)

initial_fill = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
maximal = 2**max(tap_input)-1
length = 300
initial_fill = initial_fill[:max(tap_input)]
def lfsr_generator(taps, initial_fill, length):
    register = initial_fill.copy()
    window_size = len(taps)
    output_bits = []

    for _ in range(length):
        # XOR tap bits from current register
        to_xor = [register[idx] for idx, tap in enumerate(taps) if tap == 1]
        new_bit = reduce(ixor, to_xor)
        # Shift register and append new bit
        register = register[1:] + [new_bit]

        # Optionally: take output bit as MSB or LSB — here we take the new_bit itself
        output_bits.append(register[0])

    return output_bits


gen_out = lfsr_generator(to_apply_taps, initial_fill, length)


print(maximal)
#maximal display
for i in range(0,len(gen_out),maximal):
    to_print = gen_out[i:i+maximal]
    print(to_print)
print(len(gen_out))