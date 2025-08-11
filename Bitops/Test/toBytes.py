import os

def toBytes(input_data):
    """Convert input data to bytes."""
    if isinstance(input_data, str):
        # Convert string to bytes
        return input_data.encode('utf-8')
    elif isinstance(input_data, (bytes, bytearray)):
        # If already bytes or bytearray, return as is
        return input_data
    elif isinstance(input_data, int):
        # Convert integer to bytes
        return input_data.to_bytes((input_data.bit_length() + 7) // 8, byteorder='big')
    else:
        raise TypeError("Unsupported input type. Must be str, bytes, bytearray, or int.")
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
