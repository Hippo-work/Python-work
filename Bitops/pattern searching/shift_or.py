def shift_or_search(text_bits, pattern_bits):
    """
    text_bits: list of 0/1 integers (binary data)
    pattern_bits: list of 0/1 integers (pattern to search)
    Returns: list of starting indices where pattern matches exactly
    """
    m = len(pattern_bits)
    if m == 0:
        return []

    # Step 1: Build pattern masks
    # For binary data, we only need masks for 0 and 1
    ALL_ONES = (1 << m) - 1
    mask = {0: ALL_ONES, 1: ALL_ONES}

    for i, bit in enumerate(pattern_bits):
        mask[bit] &= ~(1 << i)  # Set bit i to 0 where pattern has this symbol

    # Step 2: Initialize R
    R = ALL_ONES
    matches = []

    # Step 3: Process text
    for i, bit in enumerate(text_bits):
        R = ((R << 1) | 1) & mask[bit]
        if (R & (1 << (m - 1))) == 0:
            matches.append(i - m + 1)

    return matches


# Example usage:
text = [0, 1, 0, 1, 1, 1, 0, 1]
pattern = [1, 1, 0]
print(shift_or_search(text, pattern))
# Output: indices where pattern matches exactly