import file_in
import re
import read_bits

def xor_bits(bytearrays):
    print("--xor_bits--")
    """ It was too hard to XOR bytes, so we unpack, XOR and repack bits instead, see how this goes"""

    # get user input for XOR value
    user_input = input("Enter a value to XOR with the data; 0xHEX or 0bBINARY: ")

    while True:
		# Check for hex (e.g., 0x1A or 0X1A)
        is_hex = re.fullmatch(r"0[xX][0-9a-fA-F]+", user_input) is not None

		# Check for binary (e.g., 0b1010 or 0B1010)
        is_bin = re.fullmatch(r"0[bB][01]+", user_input) is not None


        """ it seems too hard to xor bytes, so will unpack and repack bits"""
        if is_hex:
            break
        elif is_bin:
            break
        else:
            return print("Invalid input. Please enter a valid hexadecimal or binary number.")
    user_input = int(user_input, 0)  # base 0 allows hex, decimal, and binary inputs0b0
    user_input = user_input.to_bytes((user_input.bit_length() + 7) // 8, byteorder='little')
    user_input = bytearray(user_input)
    user_unpacked = read_bits.unpack_bits(user_input)
    # pad the bytearrays to the length of the longest one
    while len(user_unpacked) <= len(bytearrays):
        user_unpacked.append(0)
    else: 
        bytearrays.append(0)

    print(user_unpacked)
    print(type(user_input))
    xor = []
    for i in range(0, len(bytearrays)):
        xor_bits = bytearrays[i] ^ user_unpacked[i]
        xor.append(xor_bits)
    return xor

if __name__ == "__main__":
    result = xor_bits(read_bits.unpack_bits(file_in.input[0]))
    print(f"XOR bit list:  {result}")
    if result:
        print(f"XOR repacked: {read_bits.pack_bits(result).hex()}")

"""
Bugs:
- user input is not checked for length, so if the user inputs a very long number, it will cause an error.
- The code does not handle cases where the input bytearrays are empty very well.
- The code does not handle cases where the input bytearrays are not of the same length.
- when changing the user input to an int, breaks if the value is too large.
"""
