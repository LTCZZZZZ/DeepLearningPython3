# 基于马尔科夫链的近似采样
# 1.我们首先要寻找以目标分布π为平稳分布的马尔科夫链，而且这个马尔科夫链的平稳分布是唯一的，找到他的各个状态的转移概率矩阵P。
#
# 2.针对这个马尔科夫链，我们设定燃烧期m和稳定期N，随机初始一个状态，在转移概率矩阵的框架下，在状态间进行m + N次的随机游走，并记录下每次转移的状态。
#
# 3.抛弃掉前面m次燃烧期采样得到的状态，只保留后面平稳期的N次采样结果，这N次采样结果就近似于目标分布π的采样。
import numpy as np
from scipy.stats import uniform
import random


def randomstate_gen(cur_state, transfer_matrix):
    # print(cur_state)
    uniform_rvs = uniform().rvs(1)  # 产生均匀分布随机数来模拟这个采样过程
    # print(uniform_rvs)
    i = cur_state - 1
    if uniform_rvs[0] <= transfer_matrix[i][0]:
        return 1
    elif uniform_rvs[0] <= transfer_matrix[i][0] + transfer_matrix[i][1]:
        return 2
    else:
        return 3


transfer_matrix = np.array([[0.7, 0.1, 0.2],
                            [0.3, 0.5, 0.2],
                            [0.1, 0.3, 0.6]], dtype='float32')
m = 10000
N = 100000

cur_state = random.choice([1, 2, 3])
state_list = []
for i in range(m + N):
    state_list.append(cur_state)
    cur_state = randomstate_gen(cur_state, transfer_matrix)

state_list = state_list[m:]

print(state_list.count(1) / float(len(state_list)))
print(state_list.count(2) / float(len(state_list)))
print(state_list.count(3) / float(len(state_list)))

