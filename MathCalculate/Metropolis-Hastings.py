# Metropolis-Hastings采样算法
# 对于目标采样分布π(x)：
#
# 第一步：随机选定一个起始点x，指定燃烧期m和稳定期N。
#
# 第二步：开始采样，每一轮采样都以上一轮的采样值x为均值，方差为1，生成一个正态分布，然后在这个正态分布中依概率随机选取一个值x'。
#
# 第三步：在[0,1]的均匀分布中随机生成一个数U，并指定接收概率α=min{1, π(x')/π(x)}，
# 如果U < α，则本轮新的采样值为x = x'，否则本轮新的采样值仍为上一轮的x。
#
# 重复第二步~第三步采样过程m + N次，结束后，保留后N次采样结果作为目标分布的近似采样。

import random
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import seaborn

seaborn.set()


# 目标采样分布pi
def pi(x):
    return (0.3 * np.exp(-(x - 0.3) ** 2) + 0.7 * np.exp(-(x - 2.) ** 2 / 0.3)) / 1.2113


m = 10000  # 燃烧期样本数
N = 100000  # 实际保留的有效样本数
sample = [0 for i in range(m + N)]  # 采样数组

sample[0] = 2  # 任选一个起始点，选择默认的0也可以，效果一样
# 基于接受概率，在建议马尔科夫链上随机游走采样
for t in range(1, m + N):
    x = sample[t - 1]
    x_star = norm.rvs(loc=x, scale=1, size=1)[0]  # 生成下一时刻随机游走的点x*
    alpha = min(1, (pi(x_star) / pi(x)))  # 接受概率

    u = random.uniform(0, 1)  # 生成满足0~1之间均匀分布的随机数
    if u < alpha:  # 接受-拒绝的过程
        sample[t] = x_star
    else:
        sample[t] = x

x = np.arange(-2, 4, 0.01)
plt.plot(x, pi(x), color='r')  # 实际目标分布
plt.hist(sample[m:], bins=100, density=True, color='b', edgecolor='k', alpha=0.6)  # 实际分布的近似采样
plt.show()
