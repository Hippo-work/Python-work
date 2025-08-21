import numpy as np

###rows columns
###fetch stuff
### col delta
### numpy decent at it
def block_interleaver(data, rows=0, columns=0):
    assert len(data) == rows * columns, "Data length must match interleaver size"
    matrix = np.reshape(data, (rows, columns))
    interleaved = matrix.T.flatten() #transpose and flatten
    return interleaved

def block_deinterleaver(data, rows, columns):
    assert len(data) == rows * columns, "Data length must match interleaver size"
    matrix = np.reshape(data, (columns, rows)).T
    deinterleaved = matrix.flatten()
    return deinterleaved

#data
data = np.array([0,1,2,3,4,5,6,7,8,9], dtype=np.uint8)
print("Data: ", data)

#interleave
interleaved = block_interleaver(data,2,5)
print("interleaved: ", interleaved)

#de-int
restored = block_deinterleaver(interleaved, 2, 5)
print("Restored: ", restored)