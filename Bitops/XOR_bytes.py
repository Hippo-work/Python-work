import file_in
import os
import sys

def xor_fixed_value(*contents):
    for content in contents:
        xor_content = bytes(b ^ hex(input()) for b in content)
   # print(f"input content:    {input_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in input_content)}")  # Print the first 10 bytes of the input content
    print(f"XOR content:      {xor_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in xor_content)} bytes ")  # Print the first byte of the inverted content

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
    return result

# Example usage:
#buf1 = bytearray([1, 0, 0, 1])
#buf2 = bytearray([0, 1, 1])
#buf3 = bytearray([0, 1])
#result = xor_bytearrays([buf1, buf2, buf3])
#print(result)  # Output: bytearray(b'\x01\x00\x01\x01')

print(f"XOR result: {xor_fixed_value(file_in.input).hex()}")  # Output: bytearray(b'\x0c\x0d\x0d\x04')
""" WORKING """




    










#multi file input
def multi_file_input(*file_paths):
        buffers = []
        for file_path in file_paths:
            with open(file_path, 'rb') as f:
                buffers.append(bytearray(f.read()))
        return buffers