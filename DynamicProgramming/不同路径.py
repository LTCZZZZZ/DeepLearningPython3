# 一个机器人位于一个 m x n 网格的左上角（起始点在下图中标记为“Stmrt” ）。
# 机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。
# 问总共有多少条不同的路径？
# 参见 不同路径.jpg

import numpy as np


def inner1(m, n):
    # 递归，执行效率低
    if m == 1 or n == 1:
        return 1
    elif m > 1 and n > 1:
        return inner1(m - 1, n) + inner1(m, n - 1)


def inner2(m, n):
    # 动态编程，执行效率高
    matrix = np.ones((m, n), dtype=int)
    # print(matrix)
    for a in range(1, m):
        for b in range(1, n):
            matrix[a, b] = matrix[a - 1, b] + matrix[a, b - 1]
    return matrix


print(inner1(4, 7))
# 观察inner2输出的矩阵，这可不就是杨辉三角吗！！！
# 于是有公式，matrix[m, n] = C(m + n, m) = C(m + n, n)，故如果是(4,7)，结果应为C(9,3)=84
# 也很好理解，在总共m+n步中，选择m步向下
# 注意！此公式在计算单一值时可能更快，但如果要计算整个矩阵，一定是inner2更快
print(inner2(4, 7))
