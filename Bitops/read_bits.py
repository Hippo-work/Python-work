import file_in
import os
import sys 

def read_bits(byte_arr):
    print("Reading bits from byte array:")
    for byte_index, byte in enumerate(byte_arr):
        print(f"Byte {byte_index}: ", end=" ")
        for bit_index in range(8):
            # Shift right and mask with 1 to get the bit
            bit = (byte >> (7 - bit_index)) & 1
            print(bit, end=" ") 
        print()  # Newline after each byte

# Example usage:
if __name__ == "__main__":
    #buf = bytearray([0b10101010, 0b1, 0xff])
    buf = file_in.input[1] # Assuming buff is a list of bytearrays
    read_bits(buf)