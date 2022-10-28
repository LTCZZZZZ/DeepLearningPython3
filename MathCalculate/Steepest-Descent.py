from sympy import *
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig, auto_add_to_figure=False)
fig.add_axes(ax)


def get_func_val(f, p):
    """
    函数的作用是将点坐标p=[x_1,x_2]的值，实际带入到符号函数中，得到函数的最终取值
    """
    return f.subs(x1, p[0]).subs(x2, p[1])


def grad_l2(grad_cur, p_cur):
    """
    函数的目标是计算出当前点处梯度的模长，grad_cur是一个用符号表示的梯度表达式，p_cur是点坐标
    """
    return sqrt(get_func_val(grad_cur[0], p_cur) ** 2 +
                get_func_val(grad_cur[1], p_cur) ** 2)


def get_alpha(f):
    """
    get_alpha函数默认在a>0的一小段领域内，f(x)的值一定减小，于是f'(x)一定小于0
    所以取使得f'(x)=0的a的最小正值，虽然这个值不一定存在。

    下面是文章中的解释：
    这里有一个隐含的条件，由于我们是沿着负梯度的方向向前走，因此，a必须满足大于0，同时，在刚刚开始走的一段时间里，
    负梯度方向决定了函数值是不断减小的，换句话说开始走的一段一定是下坡路，因此我们碰到的第一个极值点，一定是极小值点。

    那么，我们通过让一阶导函数f'(a)=0得到的一系列解当中，最小的正数解就是我们要找的步长α，他让我们跨到第一个局部极小值点，
    而函数get_alpha(f)干的就是这个事儿。

    当然我们使用前面介绍的牛顿法、割线法去迭代寻找α也都是可以的，可以尝试进行替换。
    """
    print(f)
    alpha_list = np.array(solve(diff(f)))
    return min(alpha_list[alpha_list > 0])


def func(x1, x2):
    # return x1 + x2  # 此时无解
    return 2 * x1 ** 2 + x2 ** 2 - x1 * x2 - 2 * x2


x1 = np.arange(-1.5, 1.5, 0.01)
x2 = np.arange(-1.5, 1.5, 0.01)
x1, x2 = np.meshgrid(x1, x2)
ax.plot_surface(x1, x2, func(x1, x2), color='y', alpha=0.3)

x1 = symbols("x1")
x2 = symbols("x2")
# f = x1 + x2  # 此时无解
f = 2 * x1 ** 2 + x2 ** 2 - x1 * x2 - 2 * x2

p0 = np.array([0, 0])
p_cur = p0
# grad_cur是一个用符号表示的梯度表达式
grad_cur = np.array([diff(f, x1), diff(f, x2)])
# print(grad_cur)  # [4*x1 - x2, -x1 + 2*x2 - 2] object

while True:
    ax.scatter(float(p_cur[0]), float(p_cur[1]), func(float(p_cur[0]), float(p_cur[1])), color='r')
    if (grad_l2(grad_cur, p_cur) < 0.001):
        break
    grad_cur_val = np.array([get_func_val(grad_cur[0], p_cur), get_func_val(grad_cur[1], p_cur)])
    a = symbols('a')
    # 注意：如果grad_cur_val=0，则get_alpha将会是无解的
    # 而如果f是一个平面，没有极小值，get_alpha也无解
    p_val = p_cur - a * grad_cur_val
    alpha = get_alpha(f.subs(x1, p_val[0]).subs(x2, p_val[1]))
    p_cur = p_cur - alpha * grad_cur_val

plt.show()
