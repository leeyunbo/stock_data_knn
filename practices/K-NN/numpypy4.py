import numpy as np


arr = np.arange(32).reshape((8,4))
print(arr)

print(arr[[1,5,7,2],[0,3,1,2]])

print(arr[np.ix_([1,5,7,2],[0,3,1,2])])

print(arr[[1,5,7,2]][:,[0,3,1,2]])

