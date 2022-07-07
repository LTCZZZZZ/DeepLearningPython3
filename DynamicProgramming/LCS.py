# 最长公共子序列 The longest common subsequence（LCS）
# 最长公共子序列问题是一个经典的计算机科学问题，也是数据比较程序，比如Diff工具，和生物信息学应用的基础。
# 它也被广泛地应用在版本控制，比如Git用来调和文件之间的改变。

# 下面一行表述存疑，待考证
# 该算法的空间、时间复杂度均为O(n^2)，经过优化后，空间复杂度可为O(n)，时间复杂度可为O(nlogn)

# 适用于动态规划解决的问题的特点
# * 符合「最优子结构」原则：DP 状态最优值由更小规模的 DP 状态最优值推出
# * 符合「无后效性」原则：状态的得到方式，不会影响后续其它 DP 状态取值

from functools import lru_cache  # 缓存递归的结果


@lru_cache(maxsize=128)
def LCS0(s1, s2):
    """
    从首字符开始比较，如果相同，递归之，若不同，则为res1和res2中更长的那个
    这是最蠢的版本，因为有很多重复计算，粗暴解决的话，可以加上lru_cache
    """
    if len(s1) == 0 or len(s2) == 0:
        return ''
    if s1[0] == s2[0]:
        return s1[0] + LCS0(s1[1:], s2[1:])
    else:
        res1 = LCS0(s1[1:], s2)
        res2 = LCS0(s1, s2[1:])
        if len(res1) >= len(res2):  # 可能会有=的情况，此时res1，res2均可作为结果，只看更偏重那边
            return res1
        else:
            return res2


if __name__ == '__main__':
    print(LCS0.cache_info())
    print(LCS0('BDCABA', 'ABCBDAB'))
    print(LCS0.cache_info())  # 可以看出，命中缓存16次
