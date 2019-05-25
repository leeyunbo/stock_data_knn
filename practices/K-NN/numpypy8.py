import numpy as np
import random
import matplotlib.pyplot as plt

position = 0
walk = [position]
steps = 100
zeroCnt = 0

for i in range(steps):
    position += np.random.randint(-2,3)
    walk.append(position)
    if position == 0:
        zeroCnt += zeroCnt

print(walk)
print('최저계단 : %d, 최대계단 : %d' %(min(walk),max(walk)))
print('다시 계단 0으로 돌아오는 회수 %d' %(zeroCnt))
plt.figure()
plt.plot(walk)
plt.show()






