'''
#If chunks are independent, speed up with concurrent.futures:
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_chunk, c) for c in chunks]
    results = [f.result() for f in futures]
#CPU‑bound? Switch to ProcessPoolExecutor to bypass the GIL
'''

import concurrent.futures
import random 
import datetime
import time
import uuid

def do_something(seconds, name):
	print(f"Sleeping {seconds}\t{name}\t{str(datetime.datetime.now())[:19][11:]}")
	time.sleep(seconds)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
	for i in range(50):
		executor.submit(do_something
			, seconds = random.randint(1,6)
			, name = str(uuid.uuid4())[:6].upper())