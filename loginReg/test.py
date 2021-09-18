lst = [('kapil',), ('simran',)]
dct = {}
print("Before appending data to dictonary: ",dct)
for i in range(len(lst)):
    dct[i] = lst[i][0]
print("After appending data to dictonary: ",dct)