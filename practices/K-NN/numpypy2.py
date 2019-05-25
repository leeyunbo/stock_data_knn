import numpy as np

arr = np.array([np.arange(1,5), np.arange(6,10)])
print(arr)

arr2 = arr + arr
print(arr2)
print(arr*arr2)
print(arr * 3)

arr = np.array(np.arange(10))
print(arr)

arr2 = arr[0:4]
arr2[0] = 123
print(arr2)
print(arr)
print('-'*50)

arr2d =  np.array([[1,2,3],[4,5,6],[7,8,9]])
print(arr2d[2])
print(arr2d[0][2])
print(arr2d[0,2])
arr3d = np.array([[[1,2,3],[4,5,6]], [[7,8,9],[10,11,12]]])
print(arr3d)
print(arr3d[0])

old_values = arr3d[0].copy()
arr3d[0] = 42
print(arr3d)

arr3d[0] = old_values
print(arr3d)
print(arr3d[1,0])
#---------------------------------------------------------------------------

print('-'*50)

