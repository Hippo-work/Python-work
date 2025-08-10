import file_in
import os
import sys 

def unpack_bits(byte_arr):
    print("--unpack_bits--")
    print("Reading bits from byte array:")
    #create a list to hold the bits
    bits = []
    for byte_index, byte in enumerate(byte_arr):
        print(f"Byte {byte_index}: ", end="\n")
        for bit_index in range(8):
            # Shift right and mask with 1 to get the bit
            bit = (byte >> (7 - bit_index)) & 1
            print(bit, end=" ") 
            bits.append(bit)
            if __name__ == "__main__":
                print(f"Bits so far: {bits}")  # Print the bits collected so far
        print()  # Newline after each byte
    print(f"Bit list: {bits}")
    return bits

#test the unpack_bits function
if __name__ == "__main__":
    #buf = bytearray([0b10101010, 0b1, 0xff])
    buf = file_in.input[1] # Assuming buff is a list of bytearrays
    bit_out = unpack_bits(buf)
    print(bit_out)


def pack_bits(bits):
    """Packs a list of bits into a bytearray."""
    print("--pack_bits--")
    packed = bytearray()
    #pad the bits to make sure they are a multiple of 8
    while len(bits) % 8 != 0:
        bits.append(0)
    #checks if bits are already a bytearray
    if isinstance(bits, bytearray):
        raise TypeError("Input must be a list of bits, not a bytearray.")
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
        packed.append(byte)
    return packed

#test the pack_bits function
if __name__ == "__main__":
    pack = pack_bits(bit_out)  # Assuming pack is a list of bits
    print(f"Packed bytes: {pack.hex()}")