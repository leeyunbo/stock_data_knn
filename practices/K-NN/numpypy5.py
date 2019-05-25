import numpy as np

arr = np.arange(15).reshape((3,5))
print(arr)
print(arr.T)

arr = np.random.randn(6,3)
print(np.dot(arr.T,arr))

