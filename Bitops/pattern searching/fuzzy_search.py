from fuzzysearch import find_near_matches
import numpy as np
import time
data = bytes(np.random.randint(0,2, size=1000000))
# data = ([0,1,0,1,1,1,0,0,0,1,1,1,0,1])
pattern = bytes([0,1,1,1])
start_time = time.time()
matches = find_near_matches(pattern, data, max_l_dist=1)
# print(matches)
for m in matches:
    print(m.start, m.matched)

end_time = time.time()
print(end_time - start_time)