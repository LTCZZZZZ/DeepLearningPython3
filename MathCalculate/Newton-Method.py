# 牛顿法求函数的极值点，比最速下降法更快收敛，但是需要求二阶导数
# 另有共轭梯度法，介于2者之间，而单纯的梯度下降法则是最慢的，但它在参数众多时有更好的工程性解决方案（I don't even know what I am talking about...）

from sympy import *
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)


def func(x1, x2):
    return 2 * x1 ** 2 + x2 ** 2 - x1 * x2 - 2 * x2


def zero(x1, x2):
    return 0 * x1


x1 = np.arange(-1.5, 1.5, 0.01)
x2 = np.arange(-1.5, 1.5, 0.01)
x1, x2 = np.meshgrid(x1, x2)
ax.plot_surface(x1, x2, func(x1, x2), color='y', alpha=0.3)
# 补一个零平面辅助观察图像
ax.plot_surface(x1, x2, zero(x1, x2), color='k', alpha=0.3)

x1 = symbols("x1")
x2 = symbols("x2")
# f = 2 * x1 ** 2 + x2 ** 2 - x1 * x2 - 2 * x2
f = func(x1, x2)
p0 = np.array([0, 0], dtype=float)
p_cur = p0
max_iter = 10000

for i in range(max_iter):
    # 梯度
    grad_cur = np.array([diff(f, x1).subs(x1, p_cur[0]).subs(x2, p_cur[1]),
                         diff(f, x2).subs(x1, p_cur[0]).subs(x2, p_cur[1])], dtype=float)

    # 画出并打印当前点
    ax.scatter(float(p_cur[0]), float(p_cur[1]), float(f.subs(x1, p_cur[0]).subs(x2, p_cur[1])), color='r')
    print(p_cur)

    # 终止条件
    if np.linalg.norm(grad_cur, ord=2) < 0.0001:
        break

    # 黑塞矩阵
    hessian_M = np.array([[diff(f, x1, 2).subs(x1, p_cur[0]).subs(x2, p_cur[1]),
                           diff(f, x1, 1, x2, 1).subs(x1, p_cur[0]).subs(x2, p_cur[1])],
                          [diff(f, x2, 1, x1, 1).subs(x1, p_cur[0]).subs(x2, p_cur[1]),
                           diff(f, x2, 2).subs(x1, p_cur[0]).subs(x2, p_cur[1])]],
                         dtype=float)

    # 黑塞矩阵求逆
    hessian_inv = np.linalg.inv(hessian_M)

    # 按牛顿法计算出的公式迭代
    p_cur = p_cur - np.dot(hessian_inv, grad_cur)

plt.show()
