import file_in
import os
import sys

def invert_file(content):# output_file):
    input_content = bytes(content)
    inverted_content = bytes(~b & 0xFF for b in content)
    #with open(output_file, 'wb') as file:
       # file.write(inverted_content)
    print(f"input content:    {input_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in input_content)}")  # Print the first 10 bytes of the input content
    print(f"inverted content: {inverted_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in inverted_content)} bytes inverted from {file_in.input}.")  # Print the first byte of the inverted content

invert_file(file_in.read_file(file_in.input))  # Use the input from file_in.py