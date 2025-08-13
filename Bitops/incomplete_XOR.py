import file_in
import re
import read_bits
import align

def xor_bits(bytearrays):
    print("--xor_bits--")
    """ It was too hard to XOR bytes, so we unpack, XOR and repack bits instead, see how this goes"""

    # get user input for XOR value
    user_input = align.left_align_hexbin_string_to_bytearray(input("Enter a value to XOR with the data; 0xHEX or 0bBINARY: "))

    #user_input is now a bytearray
    #XOR bytearrays
    print((bytearrays))
    #


    print((user_input_padded))
    print((bytearrays))

    #xor function
    xor_bytes = bytearray()
    for i, byte in enumerate(bytearrays):
        xor_bits = bytearrays[i] ^ user_input_padded[i]
        xor_bytes.append(xor_bits)
    return xor_bytes

if __name__ == "__main__":
    result = xor_bits(file_in.input[0])
    print(f"XOR bit list:  {result.hex()}")

"""
Bugs:
- user input is not checked for length, so if the user inputs a very long number, it will cause an error.
- The code does not handle cases where the input bytearrays are empty very well.
- The code does not handle cases where the input bytearrays are not of the same length.
- when changing the user input to an int, breaks if the value is too large.
"""
