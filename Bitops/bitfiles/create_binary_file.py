import sys
import os

def write_binary_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

# Example: Write 0xAAAAAAAA as 4 bytes to a binary file
<<<<<<<< HEAD:Bitops/bitfiles/create_binary_file.py
new_file = (b'\xdd\x00\x00')#.to_bytes(4, byteorder='little')
write_binary_file('d.bit', new_file)
========
new_file = (b'\x00\x00\xcc')#.to_bytes(4, byteorder='little')
write_binary_file('c.bit', new_file)
>>>>>>>> origin/main:Bitops/create_binary_file.py
