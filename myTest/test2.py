# Forward-mode differentiation an Reverse-mode differentiation
# from sympy import *

# lambdify()  # 将符号转化为可用的函数


def func0(a, b):
    return (a + b) * (b + 1)


res = func0(2, 1)
print(res)

# print(func0(3, 1) - func0(2, 1))  # func0相对与a是一次的，所以这么算结果正确
# print(func0(2, 2) - func0(2, 1))  # func0相对与b是二次的，所以这么算结果错误

# print((func0(2, 1.01) - func0(2, 1)) / 0.01)  # 求极限的数值算法

def der_func0(point=(2, 1)):
    # 计算func0在point处对每个变量的偏导数，point默认值为(2,1)
    a, b = point
    c = a + b
    d = b + 1
    c_a = 1
    d_a = 0
    c_b = 1
    d_b = 1
    # e = c * d
    e_c = d
    e_d = c
    # e_a = c_a * d + c * d_a
    e_a = e_c * c_a + e_d * d_a

    e_b = e_c * c_b + e_d * d_b
    print(e_a, e_b)


der_func0(point=(2, 1))
