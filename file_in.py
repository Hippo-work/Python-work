import sys
import os

#input = sys.argv[1] if len(sys.argv) > 1 else 'file_in.py'
input = 'a.bit'

def read_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'rb') as file:
        content = file.read()
    return content

read_file(input)

def process_content(content):
    if not content:
        raise ValueError("The file is empty.")
    # Example processing: count the number of bytes
    byte_count = len(content)
    print(f"Number of bytes in the file: {byte_count}")
    return byte_count

content = read_file(input)
byte_count = process_content(content)
print(f"Processed {byte_count} bytes from {input}.")