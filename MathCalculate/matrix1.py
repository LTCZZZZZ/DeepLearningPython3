# 线性代数，矩阵基本运算
import numpy as np
from scipy import linalg

A = np.array([[2, 1],
              [1, 2]])

# 计算矩阵特征值和特征向量（特征向量会被单位化）
# 原代码是scipy中的linalg
evalue, evector = np.linalg.eig(A)
print(evalue)
print(evector)

# 幸运的情况（虽然有相同的特征值，但特征向量组成可逆矩阵，A可对角化）
A = np.array([[1, 6, 0],
              [2, 2, 0],
              [0, 0, 5]])

evalue, evector = np.linalg.eig(A)
print(evalue)
print(evector)

# 不太走运的情况（有相同的特征值，特征向量线性相关，A无法对角化，只能求Jordan标准型）
A = np.array([[6, -2, 1],
              [0, 4, 0],
              [0, 0, 6]])

evalue, evector = np.linalg.eig(A)
print(evalue)
print(evector)

A = np.array([[0, -1],
              [1, 0]])

evalue, evector = np.linalg.eig(A)
print(evalue)
print(evector)
print(evalue.dtype)
