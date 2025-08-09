import file_in
import os
import sys

def invert_bytearrays(buffers):
    """
    XORs a list of bytearrays together, can be single or multiple files.
    Padding shorter ones with zeros.
    Inverts
    Returns a new bytearray with the result.
    """
    max_len = max(len(buf) for buf in buffers)
    # Pad each buffer to max_len with zeros
    padded = [buf + bytearray(max_len - len(buf)) for buf in buffers]
    result = bytearray(max_len)
    for i in range(max_len):
        val = 0
        for buf in padded:
            val ^= ~buf[i] & 0xff
        result[i] = val
    return result
    print(f"input content:    {input_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in input_content)}")  # Print the first 10 bytes of the input content
    print(f"inverted content: {inverted_content.hex()} Binary: {' '.join(f'{byte:08b}' for byte in inverted_content)} bytes inverted from {file_in.input}.")  # Print the first byte of the inverted content

print(f"Invert result: {invert_bytearrays(file_in.input).hex()}") 
""" WORKING """