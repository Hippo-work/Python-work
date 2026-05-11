import numpy as np

# gen_matrix = np.array([
#         [1, 0, 0, 0, 1, 1, 0],
#         [0, 1, 0, 0, 1, 0, 1],
#         [0, 0, 1, 0, 0, 1, 1],
#         [0, 0, 0, 1, 1, 1, 1]
#     ])
#
# check_matrix = np.array([
#     [1,1,0,1,1,0,0],
#     [1,0,1,1,0,1,0],
#     [0,1,1,1,0,0,1]
# ])

def create_hamming_matrices(r):
    N = 2**r - 1
    k = N - r

    P = []
    I = []
    for i in range(1,N+1):
        P.append([int(b) for b in np.binary_repr(i, width=r) if i & (i - 1) != 0][::-1])
        I.append([int(b) for b in np.binary_repr(i, width=r) if i & (i - 1) == 0][::-1])

    P = [x for x in P if x] # cleans arrays
    I = [x for x in I if x] # cleans arrays

    H = np.concat([np.array(P).T, np.array(I)], axis=1)
    G = np.concat([np.eye(4, dtype=int), np.array(P)], axis=1)

    return H, G

check_matrix, gen_matrix = create_hamming_matrices(3)


m = np.array([[0,1,1,0],[1,1,1,1],[0,0,0,0],[1,0,1,0]])

# this is a comment
def dot_product(data, matrix, modulo):
    return (data @ matrix) % modulo

def encode_7_4(data: np.array, k=4):

    enc = []
    for i in range(0,len(data),k):
        enc.append(dot_product(data[i:i+k], gen_matrix,2))
    return np.array(enc)

encoded_data = encode_7_4(m)

add_errors = encoded_data.tolist()
add_errors[0][0][0] ^= 1
add_errors[0][1][0] ^= 1
add_errors[0][2][0] ^= 1
add_errors[0][3][0] ^= 1
# add_errors[0][0][1] ^= 1
# add_errors[0][0][1] ^= 1

to_decode = np.array(add_errors).flatten()

def decode_7_4(data, N=7, k=4):
    decoded = []

    for i in range(0, len(data), N):
        word = data[i:i+N].copy()

        # syndrome
        s = dot_product(check_matrix, word, 2)
        # if syndrome is nonzero, locate bad bit
        if np.any(s):
            for bit in range(N):
                if np.array_equal(check_matrix[:, bit], s):
                    word[bit] ^= 1
                    break

        # systematic code: first 4 bits are data
        decoded.append(word[:k])

    return np.array(decoded)

decoded_data = decode_7_4(to_decode)

print(f"\nOriginal Data: \t\t{m.flatten()}", len(m.flatten()))
print(f"Encoded Data: \t\t{encoded_data.flatten()}", len(encoded_data.flatten()))
print(f"Added Errors: \t\t{np.bitwise_xor(encoded_data.flatten(), to_decode.flatten())}", len(to_decode))
print(f"Decoded Data: \t\t{decoded_data.flatten()}", len(decoded_data.flatten()))
assert np.array_equal(m, decoded_data)
