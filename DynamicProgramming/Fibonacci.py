# 有n个阶梯，一个人每一步只能跨一个台阶或是两个台阶，问这个人一共有多少种走法？
# 答案为fib(n+1)，详见爬楼梯的走法.jpg，由图可得递推公式 a(k + 2) = a(k + 1) + a(k) (k>=0)，并设a(0)=a(1)=1
# 参见 爬楼梯的走法.jpg


# 简单递归(反例)
def fib1(n):
    print(n)
    if n < 2:
        return n
    else:
        return fib1(n - 1) + fib1(n - 2)


def fib2(n):
    results = list(range(n + 1))  # 用于缓存以往结果，以便复用（目标2）

    for i in range(n + 1):  # 按顺序从小往大算（目标3）
        if i < 2:
            results[i] = i
        else:
            # 使用状态转移方程（目标1），同时复用以往结果（目标2）
            results[i] = results[i - 1] + results[i - 2]

    return results[-1]

if __name__ == '__main__':
    # result = fib1(100)  # 你等到天荒地老，它还没有执行完
    result = fib2(11)
    print(result)

