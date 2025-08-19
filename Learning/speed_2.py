import numpy as np
#If you’re working with signals or arrays, process in vectorized blocks


def process_chunk(chunk):
    # Example DSP: apply gain
    return chunk * 0.8


data = np.memmap(file, dtype=np.float32, mode="r")
chunk_size = 44100  # e.g., 1 second at 44.1kHz

for start in range(0, len(data), chunk_size):
    chunk = data[start:start+chunk_size]
    output = process_chunk(chunk)
#Benefit: Vectorization keeps the loop in C‑speed territory

