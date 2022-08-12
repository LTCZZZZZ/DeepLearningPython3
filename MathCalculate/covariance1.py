import numpy as np

# 英语，数学，物理
eng = np.array([78, 79, 72, 85, 74, 72, 70, 92, 88, 81])
mat = np.array([95, 80, 65, 90, 71, 56, 77, 84, 100, 88])
phy = np.array([98, 77, 58, 90, 75, 62, 80, 79, 99, 83])

print(eng.mean(), mat.mean(), phy.mean())
print(np.cov(eng), np.cov(mat), np.cov(phy))


S = np.vstack((eng, mat, phy))
print(S)
print(np.cov(S))  # 协方差矩阵，S的每一行表示一类数据，从pandas中读取数据时，需要转置
# print(np.cov(S.T))
print(np.corrcoef(S))  # 相关系数矩阵
