import sys
import os

def write_binary_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

# Example: Write 0xAAAAAAAA as 4 bytes to a binary file
new_file = (0xAAAAAAAA).to_bytes(4, byteorder='big')
write_binary_file('a.bit', new_file)
