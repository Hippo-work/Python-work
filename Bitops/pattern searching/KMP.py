##### KMP
def kmp_search(text, pattern):
    m, n = len(pattern), len(text)
    lps = build_lps(pattern)
    res, i, j = [], 0, 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1; j += 1
        if j == m:
            res.append(i - j); j = lps[j-1]
        elif i < n and pattern[j] != text[i]:
            if j: j = lps[j-1]
            else: i += 1
    return res

##### Horspool or BMH / Boyer-Moore
def horspool_search(text, pattern):
    m, n = len(pattern), len(text)
    skip = [m] * 256
    for k in range(m-1):  # Build skip table
        skip[pattern[k]] = m - 1 - k
    i = 0
    while i <= n - m:
        if text[i+m-1] == pattern[-1] and text[i:i+m] == pattern:
            yield i
        i += skip[text[i+m-1]]

##### Rabin Karp Algorithm
def rabin_karp(text, pattern, prime=101):
    m, n = len(pattern), len(text)
    d = 256  # size of the alphabet (byte-wise)
    p = t = 0
    h = 1
    for i in range(m-1):
        h = (h*d)%prime
    for i in range(m):
        p = (d*p + pattern[i])%prime
        t = (d*t + text[i])%prime
    for i in range(n-m+1):
        if p == t and text[i:i+m] == pattern:
            yield i
        if i < n-m:
            t = (d*(t - text[i]*h) + text[i+m])%prime
            t = (t+prime)%prime  # positive hash


#self styled dynamic skip
data = [0,1,2,3,4,5,6,7,8,9]
i = 0
while i < len(data):
    skip = 1
    print(i)
    if i == 2:
        skip = 2
    i += skip
#works