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
    最优解，这个算法细细看了一下，真是太巧妙了，这个算法的时间复杂度为O(n * c的长度)，且不要求c从小到大排列。
    动态规划法
    其实就是在当前情况下，将用上硬币c[j]与已有的最优解进行对比，如果用了之后结果更优，则更新dp[i]，得到当前最优解。
    经过一轮计算下来，就能得出全局最优解了。
    :param c: 硬币面值
    :param n: 支付金额
    :return: 最少硬币数
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    # 因为这里i是从小到大依次执行，并且显然，假如存在c[j]=i，则dp[i]=1，所以不会出现dp[i]的值被漏掉的情况
    # 所以下面的循环其实还可优化，即先对c中所有的x设置dp[x]=1，然后执行循环时若dp[i]=1则跳过
    for i in range(1, n + 1):
        for j in range(len(c)):
            if i - c[j] >= 0:
                dp[i] = min(dp[i], dp[i - c[j]] + 1)
    print(dp)
    return dp[n]


def coin2_1(c, n):
    """
    优化版，并加上得到n的最优序列
    """
    # dp[i]表示相加得到i所需的最少硬币数
    # l[i]表示相加得到i所需的最少硬币数的硬币列表
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    l = [[]] * (n + 1)
    # 先进行优化，确定dp[i]=1对应的值
    for j in c:
        if j <= n:
            dp[j] = 1
            l[j] = [j]

    for i in range(1, n + 1):
        if dp[i] == 1:
            continue
        for j in c:
            # 这里i已经不可能等于j了
            if i - j > 0:
                temp = dp[i - j] + 1
                if temp < dp[i]:
                    # 小于时进行替换，否则不操作
                    dp[i] = temp
                    l[i] = l[i - j] + [j]

    # 验证dp和l是否相符
    for i in range(n + 1):
        # print(i, l[i], dp[i])
        if dp[i] < float('inf'):
            assert dp[i] == len(l[i])
            assert i == sum(l[i])

    return dp[n], l[n]


# 遍历法（我自己写的）：
def coin3(c, n):
    """
    通过M的测试结果可知：c从小到大排列所需的运算次数大幅减少。
    但是对稍复杂的测试样例，即使先对c排序，依然无法通过，运行时间过长(5min仍未完成)，比如：
    50000 20
    1 92 1377 3168 7095 1170 1809 5046 3225 1054 4016 142 108 6430 3970 48 8416 4909 114 6968
    所以这个方法在实际使用时是行不通的。
    """
    global M
    M += 1
    # print(c, n)
    if n < 0:
        # 注意这个n<0时的返回值，很关键
        res = float('inf')
    elif n == 0:
        res = 0
    else:
        if len(c) == 1:
            if n % c[0] == 0:
                res = int(n / c[0])
            else:
                res = float('inf')
        else:
            # 这个方法不对，除了最小的硬币之外，每种硬币最多只用了一次，但是实际上，硬币可以用多次
            # res = min(coin3(c[:-1], n), 1 + coin3(c[:-1], n - c[-1]))
            # 修正为
            res = float('inf')
            for i in range(math.ceil(n / c[-1]) + 1):
                res = min(res, i + coin3(c[:-1], n - i * c[-1]))
    # print(c, n, res)  # 打印可知这里面有大量重复计算
    return res


if __name__ == '__main__':
    c = [1, 2, 7, 8, 12, 50]
    # n = 15  # 8,7
    n = 30  # 8,8,7,7

    # 特别注意：timeit不能直接当做装饰器加在递归函数中，否则每一次递归调用都会打印一次执行时间
    # 另外，注意下面括号的位置，timeit(coin2)是先将coin2变成了另一个函数（函数名变了）
    # print(timeit(coin1)(c, n))
    print(timeit(coin2)(c, n))
    print(timeit(coin2_1)(c, n))
    # M = 0
    # print(timeit(coin3)(c, n))
    # print(M)

    c = [1, 2, 5, 10]  # n=50，392次递归
    # c = [10, 5, 2, 1]  # n=50，3947次递归
    n = 50  # 10*5
    # print(coin1(c, n))  # 爆炸了，好久都运行不出结果
    print(timeit(coin2)(c, n))
    print(timeit(coin2_1)(c, n))
    # 全局变量M，记录递归次数
    # M = 0
    # print(timeit(coin3)(c, n))
    # print(M)

    c = [1, 2, 7, 8, 12, 50]
    n = 65  # 10*5
    print(timeit(coin2)(c, n))
    print(timeit(coin2_1)(c, n))
    # M = 0
    # print(timeit(coin3)(c, n))
    # print(M)
