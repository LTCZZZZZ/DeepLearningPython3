# 马尔科夫链，稳态
import numpy as np

# Ax=x，感觉稳态的分量x，就是A的特征向量，且对应的特征值为1
# 这不就是说，凡是有唯一稳态的矩阵，必存在特征值1
# 实际有唯一稳态的矩阵要求强得多：不可约，非周期，正常返
A = np.matrix([[0.7, 0.3, 0.2],
               [0.2, 0.5, 0.4],
               [0.1, 0.2, 0.4]])

B = np.matrix([[0.46808511, 0.46808511, 0.46808511],
               [0.34042553, 0.34042553, 0.34042553],
               [0.19148936, 0.19148936, 0.19148936]])

print(A @ B)
print(B @ A)

print(B@B)

print(B.T[0]@A)

evalue, evector = np.linalg.eig(A)
print(evalue)
# print(evector)
print(evector / evector[:,0].sum(axis=0))  # 果然，特征值1对应的特征向量归一化之后，就是稳态的分量x
