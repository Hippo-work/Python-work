import file_in
import os
import sys

def xor_file(content):
    input_content = bytes(content)
    xor_content = bytes(b ^ 0b1 for b in content)
    print(f"input content:    {input_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in input_content)}")  # Print the first 10 bytes of the input content
    print(f"inverted content: {xor_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in xor_content)} bytes xor from {file_in.input}.")  # Print the first byte of the inverted content

xor_file(file_in.read_file(file_in.input))  # Use the input from file_in.py