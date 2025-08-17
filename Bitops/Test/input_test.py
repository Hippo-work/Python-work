from gettext import gettext
import shlex
from typing import get_args
#attempt at default values with multi input
def get_or_default(prompt, default=0, cast=int):
    s= []
    s[:]= shlex.split(input((f"{prompt}: ").strip()))
    if safe_get(s,1) == None:
        s.append(default)
    print(s)
    return cast(s[0]) if s else default, cast(s[1])


def safe_get(seq, index, default=None):
    if -len(seq) <= index < len(seq):
        return seq[index]
    else:
        return default

'''
lr,ls = get_or_default("Learning rate")
print(type(lr))
print(type(ls))
'''
# testlist = [0,1,2]
# safe = safe_get(testlist, 3)
# print(safe)

def get_LFSR(prompt, default=1, cast=list):
    safe=[]
    safe[:]= shlex.split(input((f"{prompt}: ").strip()))
    print(safe)
    if safe_get(safe,2) == None:
        safe.extend([0 for t in range(int((max(safe[0]))))])
    print(safe)
    return safe[0], safe[1], safe[2]

taps, length, initial_fill = get_LFSR("yes: ")
print(taps,length,initial_fill)