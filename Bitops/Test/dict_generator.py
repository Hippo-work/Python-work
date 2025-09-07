import random
import json

def generate_binary_dict(num_keys=20000, min_len=5, max_len=50):
    return {
        f"key_{i}":[ ''.join(random.choice('01') for _ in range(random.randint(min_len, max_len))) ]
        for i in range(num_keys)
    }

def generate_FW_dict(num_keys=20000, min_len=5, max_len=50):
    return {
        f"key_{i}":[random.randint(10,1000)]
        for i in range(num_keys)
    }

# Example usage
binary_dict = generate_binary_dict()

with open("Bitops/dict_pattern.json", "w") as f_out:
    json.dump(binary_dict, f_out, indent=2)

fw_dict = generate_FW_dict()
with open("Bitops/dict_fw.json", "w") as f_out:
    json.dump(fw_dict, f_out, indent=2)