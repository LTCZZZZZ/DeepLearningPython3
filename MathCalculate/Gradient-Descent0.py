from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)


def f(p):
    return 0.2 * p[0] ** 2 + p[1] ** 2


def numerical_gradient(f, P):
    h = 1e-6
    x = P[0]
    y = P[1]
    dx = (f(np.array([x + h / 2, y])) - f(np.array([x - h / 2, y]))) / h
    dy = (f(np.array([x, y + h / 2])) - f(np.array([x, y - h / 2]))) / h
    return np.array([dx, dy])


def gradient_descent(cur_p, lambda_=0.1,
                     epsilon=0.0001, max_iters=10000):
    for i in range(max_iters):
        grad_cur = numerical_gradient(f, cur_p)
        if np.linalg.norm(grad_cur, ord=2) < epsilon:
            print('Gradient Descent: iter =', i)
            break
        cur_p = cur_p - grad_cur * lambda_
        ax.scatter(cur_p[0], cur_p[1], f(cur_p), color='r')

    print('局部极小值为：{}'.format(cur_p))
    return cur_p


x1 = np.arange(-4, 4, 0.01)
x2 = np.arange(-4, 4, 0.01)
print(x1.shape)
x1, x2 = np.meshgrid(x1, x2)
print(x1.shape, x2.shape)

# 注意下面这个式子，np.array([x1, x2])的shape是(2, 800, 800)，同样能调用f函数
ax.plot_surface(x1, x2, f(np.array([x1, x2])), color='y', alpha=0.3)

p0 = np.array([3, 4])
gradient_descent(p0)
plt.show()
