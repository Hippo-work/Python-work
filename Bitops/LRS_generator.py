import time
start = time.time()
import shlex

def lfsr_generator(taps:list, length:int, initial_fill=None):
    taps.sort()
    if min(taps) == 0:
        taps.pop(0)
    if initial_fill == None:
        fill=[0 for t in range((max(taps)))]
        fill.insert(0,1)
    elif initial_fill != None:
        fill = [int(f) for f in initial_fill]
        if max(fill) == 0:
            return "-:Error:- Initial of 0 gives infinite 0's"
        if len(fill) > max(taps):
            return "-:Error:- Initial fill of incorrect length, length must be less than or equal to largest tap number"
        while len(fill) <= max(taps):
            fill.append(0)
    print(f"taps: {taps}")
    print(f"fill: {fill}")
    output = []
    for _ in range(length):
        feedback = 0
        for t in taps:
            feedback ^= fill[t]
        output.append(fill[-1])
        fill = [feedback] + fill[:-1]
    return output

# #initial_fill length must = tap length #also must be binary to work
# taps =  x^4 + x + 1 ## seems the 0 tap is ommitted 
'''Gets input values from User'''
def get_LFSR(prompt, default=1, cast=list):
    safe=[]
    safe[:]= shlex.split(input((f"{prompt}: ").strip()))
    if safe_get(safe,2) == None:
        safe.append(None)
    return safe[0], safe[1], safe[2]

'''Allows default input'''
def safe_get(seq, index, default=None):
    if -len(seq) <= index < len(seq):
        return seq[index]
    else:
        return default

if __name__ == "__main__":
    '''Pulls in user taps, length and initial fill(optional)'''

    prompt =    "Enter Taps(format 0,1,2,3), then length (output bits)," \
                "then initial fill(optional): "
    taps_user, length_user, initial_fill_user = get_LFSR(prompt)
    length = int(length_user)
    taps = [int(t) for t in taps_user.split(",")]
    initial_fill = initial_fill_user

    '''Run'''
    sequence = lfsr_generator(taps, length, initial_fill)
    print(sequence)

    '''Time'''
    end = time.time()
    total_elapsed = end - start
    print(f"Elapsed time: {total_elapsed} sec")