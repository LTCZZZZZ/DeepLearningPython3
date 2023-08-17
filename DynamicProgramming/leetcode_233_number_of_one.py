# # leetcode 的第 233 号题：数字1的个数
# 给定一个整数 n，计算所有小于等于 n 的非负整数中数字 1 出现的个数。

# 对任意字符串s，长度为n，若i <= n 且 i > 0，则有 s[n-i] = s[-i]


def n_o_d_o(n):
    """
    number of digits one
    """
    if n <= 0:
        return 0
    elif n < 10:
        return 1
    else:
        res = 0
        # dp[i]表示小于10^i的所有整数中含1的个数
        length = len(str(n))
        dp = [0] * length
        for i in range(1, length):
            # 这个算法的核心关键在这里，下面都是仅需要细心分类讨论的部分
            dp[i] = 10 ** (i - 1) + dp[i - 1] * 10

        for i, num in enumerate(str(n)[::-1]):
            if int(num) == 0:
                continue
            elif int(num) == 1:
                temp = str(n)[length - i:]
                if temp:
                    # 后面那个数是比如13，从10到13的数字中1在十位上出现的次数
                    res += dp[i] * int(num) + (int(temp) + 1)
                else:
                    res += dp[i] * int(num) + 1
            else:
                res += dp[i] * int(num) + 10 ** i

            # print(res)

        print(dp)
        print(res)
        return res


if __name__ == '__main__':
    # n_o_d_o(11)
    n_o_d_o(100)
