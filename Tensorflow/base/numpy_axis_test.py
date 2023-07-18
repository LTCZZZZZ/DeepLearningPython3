# 看源码，好像是用C写了之后，在numpy/core/__init__.py文件中调用copyreg模块注册pickle实现的
# 经验证，已经可以用如下python代码实现了，不需要再用exec了，但就速度来说，肯定是numpy内部实现的更快

# 关键字：轴，axis

# np.lib.index_tricks 有许多可以简化索引的函数(和类)
# 可使用np.s_()函数来生成切片对象，或直接使用slice()函数

import numpy as np


def self_sum(m, axis=None):
    if axis is None:
        return np.sum(m)
    else:
        s = m.shape
        l = []
        for i in range(s[axis]):
            # command = 'l.append(m[' + ':,' * axis + f'{i},' + ':,' * (len(s) - axis - 1) + '])'
            # print(command)
            # exec(command)  # 问：这种取值方式不用exec怎么实现呢？？见文件头部说明

            # 直接实现
            indexes = [slice(None)] * len(s)
            indexes[axis] = i
            l.append(m[tuple(indexes)])  # 注意这里必须是元组tuple，不能是list

        return sum(l)


a = np.arange(24).reshape(2, 3, 4)
print(a)
print(self_sum(a))
print(np.sum(a, keepdims=True))

print(np.cumsum(a, axis=0))
print(np.cumsum(np.arange(12).reshape(4, 3), axis=0))  # 累积求和函数，tf中有相同函数

print(self_sum(a, axis=0))
print(np.sum(a, axis=0, keepdims=True))
print(self_sum(a, axis=1))
print(np.sum(a, axis=1, keepdims=True))
print(self_sum(a, axis=2))
print(np.sum(a, axis=2, keepdims=True))


# np.add.reduce()
print(np.sum(a, axis=(0, 1)))  # 这个功能我上面的函数没有实现，不过实现起来不难

s = np.s_[1:5:2,::3]
print(s)
