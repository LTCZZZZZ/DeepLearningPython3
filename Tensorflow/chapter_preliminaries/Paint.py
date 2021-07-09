import numpy as np
from IPython import display
from d2l import tensorflow as d2l
import tensorflow as tf


def f(x):
    return 3 * x ** 2 - 4 * x


def numerical_lim(f, x, h):
    return (f(x + h) - f(x)) / h


h = 0.1
for i in range(5):
    print(f'h={h:.5f}, numerical limit={numerical_lim(f, 1, h):.10f}')
    h *= 0.01


def use_svg_display():  # @save
    """使用svg格式在Jupyter中显示绘图。"""
    display.set_matplotlib_formats('svg')


def set_figsize(figsize=(3.5, 2.5)):  # @save
    """设置matplotlib的图表大小。"""
    use_svg_display()
    d2l.plt.rcParams['figure.figsize'] = figsize


# @save
def set_axes(axes, xlabel, ylabel, xlim, ylim, xscale, yscale, legend):
    """设置matplotlib的轴。"""
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    if legend:
        axes.legend(legend)
    axes.grid()


# @save
def plot(X, Y=None, xlabel=None, ylabel=None, legend=None, xlim=None,
         ylim=None, xscale='linear', yscale='linear',
         fmts=('-', 'm--', 'g-.', 'r:'), figsize=(3.5, 2.5), axes=None):
    """绘制数据点。"""
    if legend is None:  # 图例
        legend = []

    set_figsize(figsize)
    axes = axes if axes else d2l.plt.gca()  # gca就是get current axes的意思

    # 如果 `X` 有一个轴，输出True
    def has_one_axis(X):
        return (hasattr(X, "ndim") and X.ndim == 1 or
                isinstance(X, list) and not hasattr(X[0], "__len__"))

    if has_one_axis(X):
        X = [X]
    if Y is None:
        X, Y = [[]] * len(X), X
    elif has_one_axis(Y):
        Y = [Y]
    if len(X) != len(Y):
        X = X * len(Y)
    axes.cla()
    for x, y, fmt in zip(X, Y, fmts):
        if len(x):
            axes.plot(x, y, fmt)
        else:
            axes.plot(y, fmt)
    set_axes(axes, xlabel, ylabel, xlim, ylim, xscale, yscale, legend)
    d2l.plt.show()


x = np.arange(0, 3, 0.01)  # 直接画函数不用这种方式是怎么画的？
plot(x, [f(x), 2 * x - 3], 'x', 'f(x)', legend=['f(x)', 'Tangent line (x=1)'])


def g(x):
    return tf.sin(x)


x = np.arange(-np.pi, np.pi, 0.01)
plot(x, [g(x), np.cos(x)], 'x', 'g(x)', legend=['g(x)', "g'(x)"])

ori_x = x
# 不直接使用cos(x)，使用梯度
with tf.GradientTape() as t:
    x = tf.Variable(x)
    y = g(x)
x_grad = t.gradient(y, x)
print((x == ori_x).numpy().all())
x = tf.constant(x)  # 这一行必不可少否则会报错，后续待研究，大致原因是tf.Variable类型(或其衍生类型)可能没有len
print((x == ori_x).numpy().all())
plot(x, [g(x), x_grad], 'x', 'g(x)', legend=['g(x)', "g'(x)"])

