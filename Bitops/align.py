import re

def left_align_to_bytes_string(value_str: str) -> bytes:
    """
    Takes a string 
    representing an integer in hex (0x...), binary (0b...), or decimal,
    and returns a bytearray
    object with left-aligned bits (right-padded if needed).
    
    Example:
        '0xFFF' -> b'\xff\xf0'
        '0b1010' -> b'\xa0'
        '255' -> b'\xff'
    """
    value_str = value_str.strip().lower()

    
    # Check for hex (e.g., 0x1A or 0X1A)
    is_hex = re.fullmatch(r"0[xX][0-9a-fA-F]+", value_str) is not None
    # print(is_hex)

    # Check for binary (e.g., 0b1010 or 0B1010)
    is_bin = re.fullmatch(r"0[bB][01]+", value_str) is not None
    # print(is_bin)

    # HEX MODE
    if is_hex == True:
        if value_str.startswith('0x'):
            hex_str = value_str[2:]  # Remove '0x'
            # Pad to full bytes (2 hex digits per byte)
            if len(hex_str) % 2 != 0:
                hex_str += '0'
            return bytes.fromhex(hex_str)

    # BIN MODE
    elif is_bin == True:
        if value_str.startswith('0b'):
            bin_str = value_str[2:]
            #pad to byte boundary
            if len(bin_str) % 8 != 0:
                bin_str += '0' * (8 - len(bin_str) % 8)
            return int(bin_str, 2).to_bytes(len(bin_str) // 8, 'big')

    # DECIMAL MODE (assume binary-style padding)
    else:
        print("\n---Decimal or Error, will give funky results or break---\n")
        value = int(value_str, 10)
        bin_str = bin(value)[2:]
        if len(bin_str) % 8 != 0:
            bin_str += '0' * (8 - len(bin_str) % 8)
        return int(bin_str, 2).to_bytes(len(bin_str) // 8, 'big')

if __name__ == "__main__":
    print(bytearray(left_align_to_bytes_string(input())))   # b'\xff\xf0'
