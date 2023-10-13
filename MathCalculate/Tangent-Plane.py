# 切平面及多元微分、梯度的关系

# f=x^2*y+x*e^y，f在(2,0)处的切平面
# f'x=2xy+e^y
# f'y=x^2+xe^y
# f'x(2,0)=1
# f'y(2,0)=6
# 故切平面为p(x,y)=f(2,0)+1(x-2)+6y=x+6y

# 切平面方程很容易想象：从(2,0)出发，沿着x轴方向走则高度变化为(x-2)乘x方向的梯度1，沿着y轴方向走则高度变化为(y-0)乘y方向的梯度6，
# 于是高度的总变化即构成了切平面的方程
# f的全微分为dz=▽f·(dx,dy)+o(ρ)，忽略掉后面的o(ρ)的话，前面的部分就是切平面的方程，即在切点附近可用▽f·(dx,dy)近似代替f(x,y)的变化量

# 此外，如果想要提高精度，可以使用更高阶的泰勒多项式

from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from math import e

fig = plt.figure()
# 3.4版本后auto_add_to_figure被弃用
# ax = Axes3D(fig)
# 可使用如下代码代替
# ax = fig.add_subplot(111, projection='3d')
# 或
ax = Axes3D(fig)
fig.add_axes(ax)


def f(x, y):
    return x ** 2 * y + x * e ** y


def g(x, y):
    return x + 6 * y


ax.scatter(2, 0, f(2, 0), color='k')

x = np.arange(0, 4, 0.01)
y = np.arange(-2, 2, 0.01)
x, y = np.meshgrid(x, y)  # Return coordinate matrices from coordinate vectors
ax.plot_surface(x, y, f(x, y), color='y', alpha=0.6)

x = np.arange(1.5, 2.5, 0.01)
y = np.arange(-0.5, 0.5, 0.01)
x, y = np.meshgrid(x, y)
ax.plot_surface(x, y, g(x, y), color='b')

plt.show()
