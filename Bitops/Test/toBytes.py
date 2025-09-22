import os

def toBytes(input_data):
    """Convert input data to bytes."""
    if isinstance(input_data, str):
<<<<<<< HEAD
        #right pad hex strings to ensure they are even-length
        dat = right_pad_hex_to_bytes(input_data)
        # Convert string to bytes
        # dat = input_data.encode('utf-8')

        return dat
=======
        # Convert string to bytes
        return input_data.encode('utf-8')
>>>>>>> origin/main
    elif isinstance(input_data, (bytes, bytearray)):
        # If already bytes or bytearray, return as is
        return input_data
    elif isinstance(input_data, int):
        # Convert integer to bytes
        return input_data.to_bytes((input_data.bit_length() + 7) // 8, byteorder='big')
    else:
        raise TypeError("Unsupported input type. Must be str, bytes, bytearray, or int.")
<<<<<<< HEAD
    
if __name__ == "__main__":
    # Example usage
    input_str = 0x0f
    input_bytes = 0b10101010
    input_int = 4095
    input_bytearray = bytearray([0x01, 0x02, 0x03])

    print(input_str)
    # print(f"String: {toBytes(input_str)}")
    # print(f"Bytes: {toBytes(input_bytes)}")
    # print(f"Int: {toBytes(input_int)}")
    # print(toBytes(input_bytearray))

def right_pad_hex_to_bytes(value):
    hex_str = hex(value)[2:]  # Strip '0x'
    print((value))
    
    # If not a full byte, append '0' on the right
    if len(hex_str) % 2 != 0:
        hex_str += '0'

    return bytes.fromhex(hex_str)

print(right_pad_hex_to_bytes(0x05).hex())  # Should print b'\xf0'

def right_pad_binary_to_bytes(value: int) -> bytes:
    bin_str = bin(value)[2:]  # Remove '0b' prefix
    
    # Pad with 0s on the right until it's a multiple of 8
    padding = (8 - (len(bin_str) % 8)) % 8
    padded_bin_str = bin_str + '0' * padding

    # Convert binary string to int, then to bytes
    byte_length = len(padded_bin_str) // 8
    padded_int = int(padded_bin_str, 2)
    return padded_int.to_bytes(byte_length, byteorder='big')

print(right_pad_binary_to_bytes(0b000000001111))
=======
if __name__ == "__main__":
    # Example usage
    input_str = 0xfff
    input_bytes = b'\x01\x02\x03'
    input_int = 4095
    input_bytearray = bytearray([0x01, 0x02, 0x03])

    print(toBytes(input_str).bin())
    print(toBytes(input_bytes))
    print(toBytes(input_int))
    print(toBytes(input_bytearray))
    print(toBytes(0b101010))  # Example of binary input
    print(toBytes(0x1A2B3C).hex())
    print(toBytes(os.urandom(16)))  # Example of random bytes
    # Example of list input (should raise TypeError)
    try:
        print(toBytes([1, 2, 3]))
    except TypeError as e:
        print(e)
    # Example of unsupported type input (should raise TypeError)
    try:
        print(toBytes(3.14))  # Float input
    except TypeError as e:
        print(e)
    # Example of empty input
    print(toBytes(''))
>>>>>>> origin/main
