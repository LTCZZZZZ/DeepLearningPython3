import numpy as np
# from IPython import display
from d2l import tensorflow as d2l
# import tensorflow as tf


def normal(x, mu, sigma):
    p = 1 / np.sqrt(2 * np.pi) / sigma
    return p * np.exp(-0.5 / sigma**2 * (x - mu)**2)


# 再次使用numpy进行可视化
x = np.arange(-7, 7, 0.01)

# 均值和标准差对
# 改变均值会产生沿  𝑥  轴的偏移，增加方差将会分散分布、降低其峰值
params = [(0, 1), (0, 2), (3, 1)]
d2l.plot(x, [normal(x, mu, sigma) for mu, sigma in params], xlabel='x',
         ylabel='p(x)', figsize=(4.5, 2.5),
         legend=[f'mean {mu}, std {sigma}' for mu, sigma in params])
d2l.plt.show()
