# 看下面自己写的文字注释说明，非常重要

# https://zh-v2.d2l.ai/chapter_linear-networks/linear-regression.html
# https://www.zhihu.com/question/21813005/answer/1748109260
# https://zhuanlan.zhihu.com/p/24709748 矩阵求导术(上)
# https://zhuanlan.zhihu.com/p/24863977 矩阵求导术(下)

# X.T @ X @ w = X.T @ y，一般来说，若X.T有逆矩阵，则有 Xw = Y
# 问题是，反过来想，若X.T不可逆，则X.T @ X真的可逆吗？？？
# X列满秩时，可推导得X.T @ X可逆，但此时难道X本身还能不可逆(虽然X可能不是方阵，但它仍然可逆啊)？
# 即X列满秩时(此时必有m >= n)"应该"必存在Xi使得Xi @ X = E

# 我知道问题在哪儿了，当X不是方阵时，无论X是列满秩还是行满秩，
# 必不可能同时存在X.T和X的左逆矩阵。假设X的shape为(m, n)，则X.T的shape为(n, m)
# 若m > n，则X.T的左逆矩阵不存在；若m < n，则X的左逆矩阵不存在

# 那么第二个问题来了，既然不能在原式两边把X.T约去，那为什么下面的方法一还能行得通呢（姑且先假设一定有m > n）？
# 猜测的原因是，原式为X.T @ (Xw - Y) = 0，当X.T为满秩阵(不论行列)时，只能Xw - Y = 0
# 故首先方法一在m > n且X满秩时可用
# 当m < n且X满秩时，首先方法二就不可用，因为(X.T @ X).T就不存在，因为它是n阶非满秩方阵，
# 此时方法一的结果有一定的参考价值，因为X的左逆矩阵不存在，X.I求出的是X的右逆矩阵，
# 将w = X.I @ y代入原式可得原式成立，即w是原式的解，但不是唯一解。(此时原式的解为一解空间)  ———— 重要
# 需要注意的是：当m < n且X非满秩时，方法一的结果也不具有参考价值了(此时尚不清楚X.I是按什么规则求出来的，但确实能求出来)

import numpy as np

X = np.matrix([[0, 1, 2, 3],
               [1, 1, 2, 3],
               [1, 1, 2, 4]], dtype=float)  # shape(m, n)，有m > n
Xi = np.matrix([[-1, 0.5, 0.5],
                [1, 0, 0]], dtype=float)
y = np.array([[0, ],
              [1, ],
              [2, ]])

# print(X @ Xi)
# print(Xi @ X)
print(np.linalg.pinv(X), X.I)
print(X @ X.I)

# 方法一
w1 = X.I @ y
print(w1)

# 方法二
# w2 = (X.T @ X).I @ X.T @ y
# print(w2)
# print(X @ w2 - y)
#
# print(w1 == w2)
