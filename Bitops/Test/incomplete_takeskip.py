
##### Take skip
##### still basic setup, can't take s1t1 yet
##### r not included
##### i not included
##### z not included
##### l not included
def take_skip(bits,t=0,s=0):
    """
    check if its list or bytearray
    if bytearray, unpack
    use list splitting
    take
    skip
    reverse (r any number)
    add zeros (insert at index number)
    add ones
    """
    print(bits)
    # list[start:stop:step]
    #range(start,stop,step)
    # ts = bits[::-1]   #reverses list
    # ts = bits[:5]     #returns first 5 index (stop)
    # ts = bits[2:-2]     #drops first and last 2 index(start 2:stop 2 from end)
    # ts = bits[::2]      #drops every other list (t1s1)
    # ts = bits[::-2]     #reverses list and does t1s1

    ts = []
    # t = 4 #take value
    # s = 1 #skip value #which ends up being skip -1? #not quite, value changes if take changes
    #take 2 skip 1
    for i in range(0, len(bits), t+s):
        ts.extend(bits[i:i+t])
    return ts

#if t > s it doesnt work right, so s has to be set in relation to t
#with s set to t+s
#t1s1 = t1s1
#t2s1 = t2s1
#t1s3 = 




if __name__ == "__main__":
    test = take_skip([0,1,2,3,4,5,6,7,8,9],4,1)
    print(test)