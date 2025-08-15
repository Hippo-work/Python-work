#####################
#list slicing === list[start:stop:step]



#####################
def split_into_n_parts(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

# Example
lst = [1, 2, 3, 4, 5, 6, 7]
print(split_into_n_parts(lst, 3))
# Output: [[1, 2, 3], [4, 5], [6, 7]]


######################
def chunks(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

# Example
lst = [1, 2, 3, 4, 5, 6, 7]
print(chunks(lst, 3))
# Output: [[1, 2, 3], [4, 5, 6], [7]]


######################
def split_on_value(lst, value):
    result = []
    current = []
    for item in lst:
        if item == value:
            if current:
                result.append(current)
                current = []
        else:
            current.append(item)
    if current:
        result.append(current)
    return result

# Example
lst = [1, 2, 0, 3, 4, 0, 5]
print(split_on_value(lst, 0))
# Output: [[1, 2], [3, 4], [5]]


#######################
def split_at_indices(lst, indices):
    indices = [0] + indices + [len(lst)]
    return [lst[indices[i]:indices[i+1]] for i in range(len(indices)-1)]

# Example
lst = [10, 20, 30, 40, 50, 60]
indices = [2, 4]
print(split_at_indices(lst, indices))
# Output: [[10, 20], [30, 40], [50, 60]]


########################
def sliding_window(lst, size, step=1):
    return [lst[i:i+size] for i in range(0, len(lst) - size + 1, step)]

# Example
lst = [1, 2, 3, 4, 5]
print(sliding_window(lst, 3))
# Output: [[1, 2, 3], [2, 3, 4], [3, 4, 5]]

########################
#flatten a matrix
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
flat = [item for row in matrix for item in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]