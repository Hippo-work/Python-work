import file_in
##### Truncate bits
##### Works with lists and bytearray([])
def truncate_bits(bits, start=0, stop=None):
    #list slicing easy
    #stop is optional
    truncate = bits[start:stop:1]
    return truncate

if __name__ == "__main__":
    # test = [0,1,2,3,4,5,6,7,8,9] #work
    # test = bytearray([0,1,2,3,4,5,6,7,8,9]) #works
    test = file_in.input[0] #works
    print(truncate_bits(test,2))