# 硬币问题
# 现有面值为c1,c2,c3,…,cm的m种硬币，求支付n元时所需硬币的最少枚数。各面值的硬币可以使用任意次。
# 举个例子，当面值为1、2、7、8、12、50时，我们如果需要支付15元，用贪心算法来算的话，就会出现12、2、1的结果，需要三枚硬币。
# 但是事实上，我们只需要7、8元面值的两枚硬币就够了。

import math
from tools import timeit


# 遍历法：
def coin1(c, n):
    """
    不可取，对n=30就要运行好久了。
    假设c=[1,2]，n=50，对coin1函数来说，c固定，令f(n)=coin1(c, n)，则f(50)=min(f(49), f(48))+1，
    依次继续递归下去，直到n=0或负数时，返回0或inf，这样就形成了一个递归树，这个递归树的深度为n，每个节点的子节点数为c的长度，
    因为没有存储中间结果，所以这个递归树的节点数为c的长度的n次方，这个递归树的时间复杂度为O(c的长度的n次方)。
    全局递归遍历法
    :param c: 硬币面值
    :param n: 支付金额
    :return: 最少硬币数
    """
    if n == 0:
        return 0
    if n < 0:
        return float('inf')
    res = float('inf')
    for i in range(len(c)):
        res = min(res, coin1(c, n - c[i]) + 1)
    return res


# 动态规划法：
def coin2(c, n):
    """
    动态规划法
    :param c: 硬币面值
    :param n: 支付金额
    :return: 最少硬币数
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for j in range(len(c)):
            if i - c[j] >= 0:
                dp[i] = min(dp[i], dp[i - c[j]] + 1)
    return dp[n]


# 遍历法（我自己写的）：
def coin3(c, n):
    # print(c, n)
    if n < 0:
        # 注意这个n<0时的返回值，很关键
        res = float('inf')
    elif n == 0:
        res =  0
    else:
        if len(c) == 1:
            res = math.ceil(n / c[0])
        else:
            # 这个方法不对，除了最小的硬币之外，每种硬币最多只用了一次，但是实际上，硬币可以用多次
            res = min(coin3(c[:-1], n), 1 + coin3(c[:-1], n - c[-1]))
            # 修正为
            res = float('inf')
            for i in range(math.ceil(n / c[-1]) + 1):
                res = min(res, i + coin3(c[:-1], n - i * c[-1]))
    # print(c, n, res)
    return res


if __name__ == '__main__':
    c = [1, 2, 7, 8, 12, 50]
    # n = 15  # 8,7
    n = 30  # 8,8,7,7

    # 特别注意：timeit不能直接当做装饰器加在递归函数中，否则每一次递归调用都会打印一次执行时间
    # 另外，注意下面括号的位置，timeit(coin2)是先将coin2变成了另一个函数（函数名变了）
    # print(timeit(coin1)(c, n))
    print(timeit(coin2)(c, n))
    print(timeit(coin3)(c, n))

    c = [1, 2, 5, 10]
    n = 50  # 10*5
    # print(coin1(c, n))  # 爆炸了，好久都运行不出结果
    print(timeit(coin2)(c, n))
    print(timeit(coin3)(c, n))
