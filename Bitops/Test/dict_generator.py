import random
import json

def generate_binary_dict(num_keys=50000, min_len=5, max_len=50):
    return {
        f"key_{i}":[ ''.join(random.choice('01') for _ in range(random.randint(min_len, max_len))) ]
        for i in range(num_keys)
    }

# Example usage
binary_dict = generate_binary_dict()

with open("Bitops/binary_dict.json", "w") as f_out:
    json.dump(binary_dict, f_out, indent=2)