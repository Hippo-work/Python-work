# change the skip based on a result of the loop??

skip = 1
data = [0,1,2,3,4,5,6,7,8,9]

# for i in range(0,len(data), skip):
#     skip = 1
#     print(i)
#     if i == 2:
#         skip = 2
###doesnt seem to work


i = 0
while i < len(data):
    skip = 1
    print(i)
    if i == 2:
        skip = 2
    i += skip
#works

