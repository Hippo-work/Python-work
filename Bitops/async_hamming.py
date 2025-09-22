import numpy as np
import time
import asyncio
import json
import aiofiles
from multiprocessing import Pool, cpu_count

def binstr_to_bits(s):
    return [int(c) for c in s]

def bits_to_int(bits):
    x = 0
    for b in bits:
        x = (x << 1) | (1 if b else 0)
    return x

async def async_pattern_reader(filepath, queue):
    async with aiofiles.open(filepath, "r") as fin:
        raw = await fin.read()
        dict_in = json.loads(raw)
        for key, bin_list in dict_in.items():
            bits_list = [binstr_to_bits(b) for b in bin_list]
            pattern = bits_list[0]
            max_diff = max(1, len(pattern) // 10)
            await queue.put((key, pattern, max_diff))

async def gather_patterns(filepath):
    queue = asyncio.Queue()
    await async_pattern_reader(filepath, queue)
    patterns = []
    while not queue.empty():
        patterns.append(await queue.get())
    return patterns

result = asyncio.run(gather_patterns("Bitops/dict_pattern.json"))

print(result[10])