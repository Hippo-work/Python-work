import file_in
import time
import numpy as np
start_time_jt = time.time()
def unpack_bits(byte_arr: bytearray, verbose: bool = False) -> list[int]:
    if verbose:
        print("--unpack_bits--")
        print("Reading bits from byte array:")

    bits = []
    for byte_index, byte in enumerate(byte_arr):
        if verbose:
            print(f"Byte {byte_index}: ", end="")
        for bit_index in range(8):
            bit = (byte >> (7 - bit_index)) & 1
            bits.append(bit)
            if verbose:
                print(bit, end=" ")
        if verbose:
            print()
    
    if verbose:
        print(f"Bit list: {bits}")
    return bits

#test the unpack_bits function
if __name__ == "__main__":
    #buf = bytearray([0b10101010, 0b1, 0xff])
    buf = file_in.input[0]# can only take 1 bytearray input per call
    bit_out = unpack_bits(buf, True)
    print(bit_out)


def pack_bits(bits: list[int], verbose: bool = False) -> bytearray:
    if verbose:
        print("--pack_bits--")
        print(f"Original bit length: {len(bits)}")

    if not all(bit in (0, 1) for bit in bits):
        raise ValueError("All elements must be 0 or 1.")

    if isinstance(bits, bytearray):
        raise TypeError("Input must be a list of bits, not a bytearray.")

    # Pad to multiple of 8
    padded_bits = bits + [0] * ((8 - len(bits) % 8) % 8)

    if verbose and len(padded_bits) != len(bits):
        print(f"Padded with {len(padded_bits) - len(bits)} zero(s)")

    packed = bytearray()
    for i in range(0, len(padded_bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | padded_bits[i + j]
        packed.append(byte)
        if verbose:
            print(f"Packed byte {i//8}: {byte:08b}")

    return packed

#test the pack_bits function
if __name__ == "__main__":
    pack = pack_bits(bit_out, True)  # Assuming pack is a list of bits
    print(f"Packed bytes: {pack.hex()}")
end_time_jt = time.time()
start_time_np = time.time()

'''Numpy'''
def unpack_bits_np(byte_arr: bytearray) -> np.ndarray:
    return np.unpackbits(np.frombuffer(byte_arr, dtype=np.uint8))

def pack_bits_np(bits: np.ndarray) -> bytearray:
    padded = np.pad(bits, (0, -len(bits) % 8))
    reshaped = padded.reshape(-1, 8)
    packed = np.packbits(reshaped, axis=1)
    return bytearray(packed.flatten())

if __name__ == "__main__":
    test = unpack_bits_np(buf)
    print(f"Np Unpack", test)
    print(f"Np pack", pack_bits_np(test).hex())

end_time_np = time.time()
print(f"jt:",end_time_jt - start_time_jt)
print(f"np:",end_time_np - start_time_np)
