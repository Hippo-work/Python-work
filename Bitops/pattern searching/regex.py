import re
import numpy as np
data = np.random.randint(0,2, size=100000)
patterns = [b'0111', b'0111', b'0111']
# Escape each pattern for safety, join with alternation
regex = re.compile(b'|'.join(re.escape(p) for p in patterns))

matches = list(regex.finditer(data))
print(matches)

