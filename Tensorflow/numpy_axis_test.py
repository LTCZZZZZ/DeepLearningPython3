# 看源码，好像是用C写了之后，在numpy/core/__init__.py文件中调用copyreg模块注册pickle实现的
import numpy as np


def self_sum(m, axis=None):
    if axis is None:
        return np.sum(m)
    else:
        s = m.shape
        l = []
        for i in range(s[axis]):
            command = 'l.append(m[' + ':,' * axis + f'{i},' + ':,' * (len(s) - axis - 1) + '])'
            # print(command)
            exec(command)  # 问：这种取值方式不用exec怎么实现呢？？见文件头部说明
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

# string = '''for i in range(3):
#     print(i)
#     if i > 1:
#         print("i > 1")'''
# exec(string)
