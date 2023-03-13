# 牛顿切线法求函数零点，一般来说需满足以下条件
# 1. x∈[a,b], f(a) * f(b) < 0
# 2. f'(x) ≠ 0
# 3. f''(x)在区间[a,b]上不变号，即f'(x)在区间[a,b]上单调递增或递减
# 由2，3可知f(x)在区间[a,b]上单调递增或递减，且不改变凹凸性
# 我感觉这已经是充分条件了

import numpy as np


def f(x):
    return - x ** 2 + 4


def f_prime(x):
    return -2 * x


def newton(f, f_prime, x0, tol=1e-6, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_new = x - f(x) / f_prime(x)
        delta = np.abs(x_new - x)
        print(f'delta: {delta}')
        print(f'x_new: {x_new}')
        if delta < tol:
            print(f'iter_count: {i + 1}')
            x = x_new
            break
        x = x_new
    print(x)
    return x


newton(f, f_prime, 3)
newton(f, f_prime, 1)

