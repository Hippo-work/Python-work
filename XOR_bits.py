import file_in
import os
import sys

def xor_file(*contents):
    for content in contents:
        input_content = bytes(content)
        xor_content = bytes(b ^ 0b1 for b in content)
   # print(f"input content:    {input_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in input_content)}")  # Print the first 10 bytes of the input content
    print(f"XOR content:      {xor_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in xor_content)} bytes xor from {buffer}.")  # Print the first byte of the inverted content

for i, buffer in enumerate(file_in.buff):
    print(f"Buffer {i+1}: {buffer.hex()}")  # Print the hex representation of each buffer
    xor_file(buffer)