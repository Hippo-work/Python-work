import queue, threading
import numpy as np
import time

#For real‑time DSP, you can feed chunks through a producer/consumer pattern:

q = queue.Queue(maxsize=10) # prevents runaway memory leak

def producer():
    while True:
        chunk = [1,2,3,4,5]
        q.put(chunk)

def consumer():
    while True:
        chunk = q.get()
        if chunk is None:
            break
        processed = chunk

        q.task_done()
        return processed


threading.Thread(target=producer, daemon=True).start()
threading.Thread(target=consumer, daemon=True).start()
#Great for live audio or video feeds
print(consumer())