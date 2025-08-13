import sys
import os

#input = sys.argv[1] if len(sys.argv) > 1 else 'file_in.py'
#input = 'a.bit'

#multi file input
def multi_file_input(*file_paths):
        buffers = []
        for file_path in file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            with open(file_path, 'rb') as f:
                buffers.append(bytearray(f.read()))
        return buffers

#when run from Python-work folder
input = multi_file_input('Bitops/bitfiles/a.bit')

print("--file_in--")
for i, buffer in enumerate(input):
    print(f"Buffer {i+1}: {buffer.hex()} {type(buffer)}")  # Print the hex representation of each buffer

#def read_file(file_path):
#    if not os.path.exists(file_path):
#        raise FileNotFoundError(f"The file {file_path} does not exist.")
#    with open(file_path, 'rb') as file:
#        content = file.read()
#    return content

#def process_content(content):
#    if not content:
#        raise ValueError("The file is empty.")
#    # Example processing: count the number of bytes
#    byte_count = len(content)
#    print(f"Number of bytes in the file: {byte_count}")
#    return byte_count
#
#byte_count = process_content(read_file(input))
#print(f"Processed {byte_count} bytes from {input}.")
