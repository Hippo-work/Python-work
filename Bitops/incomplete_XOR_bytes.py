import file_in
import re

def xor_byte_fixed_value(contents):
	"""
	XORs a fixed supplied value with the contents of the file.
	"""
	print("--xor_byte_fixed_value--")
	#get user input for XOR value
	user_input = input("Enter a value to XOR with the data; 0xHEX or 0bBINARY:")

	while True:
		# Check for hex (e.g., 0x1A or 0X1A)
		is_hex = re.fullmatch(r"0[xX][0-9a-fA-F]+", user_input) is not None

		# Check for binary (e.g., 0b1010 or 0B1010)
		is_bin = re.fullmatch(r"0[bB][01]+", user_input) is not None

		""" it seems too hard to xor bytes, so will unpack and repack bits"""
		if is_hex:
			user_input = int(user_input, 0)  # base 0 allows hex, decimal, and binary inputs0b0
			#convert to hex big endian
			bitlen = max(1, user_input.bit_length() // 8)
			print(f"user_input: {user_input}")
			print(f"bitlen: {bitlen}")
			user_input = bytearray(user_input.to_bytes(bitlen, byteorder='little')) 
			break

		elif is_bin:
			user_input = int(user_input, 0)  # base 0 allows hex, decimal, and binary inputs0b0
			#read bytes as binary and then xor 
			bitlen = max(1, user_input.bit_length() // 8)
			print(f"user_input: {user_input}")
			print(f"bitlen: {bitlen}")
			user_input = bytearray(user_input.to_bytes(bitlen, byteorder='little')) 
			break

		else:
			return print("Invalid input. Please enter a valid hexadecimal or binary number.")

	print(user_input.hex())
	print(type(user_input))

	contents.append(user_input)
	result = xor_bytearrays(contents)
	#print(result)
	
	return result


def xor_bytearrays(buffers):
	"""
	XORs a list of bytearrays together, padding shorter ones with zeros.
	Returns a new bytearray with the result.
	"""
	print("--xor_bytearrays--")
	max_len = max(len(buf) for buf in buffers)
	# Pad each buffer to max_len with zeros
	padded = [buf + bytearray(max_len - len(buf)) for buf in buffers]
	result = bytearray(max_len)
	for i in range(max_len):
		val = 0
		for buf in padded:
			val ^= buf[i]
		result[i] = val
		#print(f"Result: {result}")
	return result

# Example usage:
#buf1 = bytearray([1, 0, 0, 1])
#buf2 = bytearray([0, 1, 1])
#buf3 = bytearray([0, 1])
#result = xor_bytearrays([buf1, buf2, buf3])
#print(result)  # Output: bytearray(b'\x01\x00\x01\x01')

if __name__ == "__main__":
	print(f"XOR result: {xor_bytearrays(file_in.input).hex()}")  
	""" NOT WORKING """
