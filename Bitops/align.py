import re

import re

def left_align_hexbin_string_to_bytearray(value_str: str, verbose: bool = False) -> bytearray:
    """
    Converts a string representing a hex (0x...), binary (0b...), or decimal value
    into a left-aligned bytearray (right-padded with zeros if needed).
    
    Examples:
        '0xFFF'   -> bytearray(b'\xff\xf0')
        '0b1010'  -> bytearray(b'\xa0')
        '255'     -> bytearray(b'\xff')
    """
    value_str = value_str.strip().lower()

    if verbose:
        print(f"Input string: {value_str}")

    # HEX MODE
    if re.fullmatch(r"0x[0-9a-f]+", value_str):
        hex_str = value_str[2:]
        if len(hex_str) % 2 != 0:
            hex_str += '0'
            if verbose:
                print(f"Padded hex string: {hex_str}")
        return bytearray.fromhex(hex_str)

    # BIN MODE
    elif re.fullmatch(r"0b[01]+", value_str):
        bin_str = value_str[2:]
        pad_len = (8 - len(bin_str) % 8) % 8
        bin_str += '0' * pad_len
        if verbose:
            print(f"Padded binary string: {bin_str}")
        return int(bin_str, 2).to_bytes(len(bin_str) // 8, 'big')

    # DECIMAL MODE
    elif re.fullmatch(r"\d+", value_str):
        value = int(value_str)
        bin_str = bin(value)[2:]
        pad_len = (8 - len(bin_str) % 8) % 8
        bin_str += '0' * pad_len
        if verbose:
            print(f"Decimal converted to padded binary: {bin_str}")
        return int(bin_str, 2).to_bytes(len(bin_str) // 8, 'big')

    else:
        raise ValueError(f"Unrecognized format: {value_str}")

if __name__ == "__main__":
    # print(left_align_hexbin_string_to_bytearray(input("\nEnter in format 0xHex or 0bBinary: ")))   # b'\xff\xf0'
    print(left_align_hexbin_string_to_bytearray("0b101"))


###how about i just convert it straight to a list, then it shouldnt have to bytebound it
    