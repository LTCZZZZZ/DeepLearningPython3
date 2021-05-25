# 单变量的梯度下降法（牛顿切线法一般是用于求函数零点的）
# 以y=x^2为例，注意此x和下面neuron中的x完全不同

import numpy as np


def func(z):
    return z ** 2


class neuron:

    def __init__(self, w):
        self.w = w

    def __call__(self, x=1):  # 输入默认值设为1
        self.x = x
        return func(self.w * x)


n = neuron(0.6)
# print(n())

eta = 0.15

i = 0
while True:
    y = n()
    print(y, n.w)
    if y < 0.1:
        break

    # 这两行是直接用y当做了损失函数
    # delta_w = -eta * y * (1 - y) * n.x
    # delta_b = -eta * y * (1 - y)

    # 下面两行是一般常用的损失函数，即二范数
    delta_w = -eta * y * n.x

    n.w += delta_w
    i += 1

print(i)
