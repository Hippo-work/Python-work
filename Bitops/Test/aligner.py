#AI

"""
In Progress, needs editing from align.py
"""
import argparse

def left_align_to_bytes_auto(value_str: str) -> bytes:
    """
    Takes a string representing an integer in hex (0x...), binary (0b...), or decimal,
    and returns a bytes object with left-aligned bits (right-padded if needed).
    """
    value_str = value_str.strip().lower()

    # HEX MODE
    if value_str.startswith('0x'):
        hex_str = value_str[2:]  # Remove '0x'

        # Pad to full bytes (2 hex digits per byte)
        if len(hex_str) % 2 != 0:
            hex_str += '0'
        return bytes.fromhex(hex_str)

    # BIN MODE
    elif value_str.startswith('0b'):
        bin_str = value_str[2:]
        if len(bin_str) % 8 != 0:
            bin_str += '0' * (8 - len(bin_str) % 8)
        return int(bin_str, 2).to_bytes(len(bin_str) // 8, 'big')

    # DECIMAL MODE (assume binary-style padding)
    else:
        print("Decimal or other detected, maybe break or give funky results")
        value = int(value_str, 10)
        bin_str = bin(value)[2:]
        if len(bin_str) % 8 != 0:
            bin_str += '0' * (8 - len(bin_str) % 8)
        return int(bin_str, 2).to_bytes(len(bin_str) // 8, 'big')


def main():
    parser = argparse.ArgumentParser(
        description="Convert a hex/bin/dec integer to left-aligned bytes (padded if needed)."
    )
    parser.add_argument(
        "value",
        type=str,
        help="Input value (hex: 0x..., binary: 0b..., or decimal)"
    )
    parser.add_argument(
        "--hex", action="store_true",
        help="Also print the result as a hex string"
    )
    args = parser.parse_args()

    try:
        result = left_align_to_bytes_auto(args.value)
        print("Bytes:", result)
        if args.hex:
            print("Hex:  ", result.hex())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()

##bash
# $ python aligner.py --value 0xFFF --mode hex
# b'\xff\xf0'

# $ python aligner.py --value 0x1 --mode bin
# b'\x80'