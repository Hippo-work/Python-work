#### lets try manual convolution to learn eh
#start with numpy so we get the right answer
import numpy as np
import random
rand_array1 = [random.randint(0, 99) for _ in range(10000)]
rand_array2 = [random.randint(0, 99) for _ in range(10000)]

import time
start_time_np = time.time()
np_test = np.convolve(rand_array1,rand_array2)
end_time_np = time.time()
# print(np_test)
####3blue1brown said, take 2 1d matrix e.g. (1,2,3) x (4,5,6)
#### flip the second (1,2,3) x (6, 5, 4)
### multiply each one together? then add them i think
##suuuper manual way first
#TABLE WAY
#     4   5   6
# 1   4   5   6
# 2   8   10  12
# 3   12  15  18
# them add up diagonally SW to NE
term_1 = 4
term_2 = 8 + 5
term_3 = 12 + 10 + 6
term_4 = 15 + 12
term_5 = 18
final_val = [term_1, term_2, term_3, term_4, term_5]
# print(final_val)
# also
#     (1,2,3)
# (6,5,4)
t_1 = 1*4
#     (1,2,3)
#   (6,5,4)
t_2 = 1*5 + 2*4
#     (1,2,3)
#     (6,5,4)
t_3 = 1*6 + 2*5 + 3*4
#     (1,2,3)
#       (6,5,4)
t_4 = 2*6 + 3*5
#     (1,2,3)
#         (6,5,4)
t_5 = 3*6
final_t = [t_1, t_2, t_3, t_4, t_5]
# print(final_t)
#lets try a loop if poss, might need to pad the loop maybe
start_time_jt = time.time()
def janky_jt_convolution(arr1, arr2):
    i=0
    while i < len(arr1):
        arr2.append(0)
        i+=1
    f_a = []
    for i in range(len(arr1)):
        for j in range(len(arr2)):
            x = arr1[i] * arr2[j]
            f_a.append(x)
    answer = []
    for i in range(0,len(arr2)-1):
        answer.append(sum(f_a[i::len(arr2)-1]))
    return answer

janky_jt_convolution(rand_array1,rand_array2)
end_time_jt = time.time()

total_time_np = end_time_np - start_time_np
total_time_jt = end_time_jt - start_time_jt
print(f"np:", total_time_np)
print(f"jt:", total_time_jt)
#working out below

'''

a1 = [1,2,3]
a2 = [4,5,6,0,0,0] 
f_a = []
for i in range(len(a1)):
    for j in range(len(a2)):
        x = a1[i] * a2[j]
        f_a.append(x)
print(f_a)
#split them back up into 3(window lendth)
#123
#0456
#00789
#just straight add them up vertically wow
i=0
seperated = []
while i < len(f_a):
    seperated.append(f_a[i:i+5:1])
    i+=5
print(f"seperated",seperated)
 may not need to seperate them out now, can just do take 1 skip 4 and add values
i=0
joined= []
while i < len(seperated[0]):
    joined.append(seperated[0][i]+seperated[1][i]+seperated[2][i])
    i+=1
print(f"joined",joined)
#slice addition works too
x= []
for i in range(0,len(a2)-1):
    x.append(f_a[i]+f_a[i+5]+f_a[i+10])
print(x)
# 4 5 6 8 10 12 12 15 18
# 4
#   5   8
#     6   10    12
#            12    15
#                     18
# t1 = sum([f_a[0]])
# t2 = sum([f_a[1],f_a[3]])
# t3 = sum([f_a[2],f_a[4],f_a[6]])
# t4 = sum([f_a[5],f_a[7]])
# t5 = sum([f_a[8]])
# f_ans = [t1,t2,t3,t4,t5]
# print(f_ans)

'''
























#4x3
#   0  0  4  5   6   7  0  0
#1  0  0  4  5   6   7  0  0 
#2  0  0  8  10  12  14 0  0
#3  0  0  12 15  18  21 0  0
# t1 = 4                0                       idx [0,1,2,7,11]
# t2 = 5 + 8            1 + 4
# t3 = 6 + 10 + 12      2 + 5 + 8
# t4 = 7 + 12 + 15      3 + 6 + 9
# t5 = 14 + 18          7 + 10
# t6 = 21               11

#  4  5  6  7  8  10  12  14  12  15  18  21
#  4
#     5        8
#        6        10          12  
#           7         12          15       
#                         14          18  
#                                         21

# # 5x4
#    5  6  7  8  9
# 1 [5  6  7  8  9]
# 2 [10 12 14 16 18]
# 3 [15 18 21 24 27]
# 4 [20 24 28 32 36]
# 
# 5 6 7 8 9 10 12 14 16 18 15 18 21 24 27 20 24 28 32 36
# 
# 3x3 f_a
#     4   5   6
# 1   4   5   6
# 2       8   10  12 #insert 1 0
# 3           12  15  18 #insert 2 0
#
# 4 5 6 8 10 12 12 15 18
# 4
#   5   8
#     6   10    12
#            12    15
#                     18




