import math

import numpy as np

A = [[0, 0, 0, 2, 2],
     [0, 0, 0, 3, 3],
     [0, 0, 0, 1, 1],
     [1, 1, 1, 0, 0],
     [2, 2, 2, 0, 0],
     [5, 5, 5, 0, 0],
     [1, 1, 1, 0, 0]]

U, sigma, VT = np.linalg.svd(A)

print(U)
print(sigma)
print(VT)

# U = np.round(U, 2)
# sigma = np.round(sigma, 2)
# VT = np.round(VT, 2)
# print(U)
# print(sigma)
# print(VT)

Sigma = np.zeros((7, 5))
for i in range(len(sigma)):
    Sigma[i, i] = sigma[i]
print(Sigma)
print(np.round(U@Sigma@VT, 2))
