"""
read_bits seperates each bit
they are integers
put them into a list array
can then be searched
delta function can be applied
"""
import file_in
import read_bits
import os
import sys

# now we can apply a delta function
def delta_bits(bits):
    """Calculates the delta of a list of bits.
    The delta is the difference between consecutive bits.
    """
    print("--delta_bits--")
    deltas = []
    for i in range(0, len(bits)):
        delta = bits[i] ^ bits[i -1]
        deltas.append(delta)
    deltas.pop(0)  # Remove the first element as it has no previous bit to compare
    return deltas

if __name__ == "__main__":
    result = delta_bits(read_bits.unpack_bits(file_in.input[0]))
    print(f"Delta bit list:  {result}")
    print(f"Delta repacked: {read_bits.pack_bits(result).hex()}")  # Print the hex representation of the packed delta bits
