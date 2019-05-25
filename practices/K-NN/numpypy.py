import numpy as np

data = [0.956,-0.24,2],[0.2232,1.232,4]

data = np.array(data)

print(data)

print(data.dtype, data.ndim, data.shape)

print(np.zeros(10))

print(np.zeros((3,6)))

print(np.empty((2,3,2)))

print(np.arange(15))

arr = np.array([1,2,3,4,5])
print(arr.dtype)

arr = arr.astype(np.float64)
print(arr.dtype)
