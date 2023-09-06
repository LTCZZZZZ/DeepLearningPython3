# leetcode 的第 72 号题：
# 编辑距离，广泛运用于自然语言处理(如拼写检查，linux下的diff命令等)，生物信息学(如基因序列比对)等领域。
# 给定两个单词 word1 和 word2，计算出将 word1 转换成 word2 所使用的最少操作数 。
# 你可以对一个单词进行如下三种操作：插入一个字符 删除一个字符 替换一个字符，（换位置操作=替换*2）示例：
# 输入: word1 = "horse", word2 = "ros"
# 输出: 3
# 解释:
# horse -> rorse (将 'h' 替换为 'r')
# rorse -> rose (删除 'r')
# rose -> ros (删除 'e')

# 来源：https://www.zhihu.com/question/39948290/answer/1922158996

import time
import numpy as np
from functools import lru_cache

count = 0


@lru_cache()
def assist(w1: str, w2: str):
    """
    这个算法从头到尾是我自己想出来的，不容易，，，
    """
    global count
    count += 1

    if w1 == '':
        return len(w2)
    if w2 == '':
        return len(w1)

    if w1[0] == w2[0]:
        return assist(w1[1:], w2[1:])

    # 优化的代码，非必要，但可大幅减少计算量
    if len(w1) == len(w2) == 1:
        # 此时都为单字符且不相等
        return 1

    # 以下分别对应3种操作
    r1 = assist(w1[1:], w2) + 1  # 删除
    r2 = assist(w1, w2[1:]) + 1  # 插入
    r3 = assist(w1[1:], w2[1:]) + 1  # 替换
    # print(w1, w2, r1, r2, r3)
    # time.sleep(0.5)

    return min(r1, r2, r3)


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        return assist(word1, word2)


# dp版，同时输出变更过程
def md(w1, w2):
    """
    dp[i, j]表示w1[:i]和w2[:j]的编辑距离，显然dp[0, 0] = 0，dp[0, j] = j，dp[i, 0] = i
    """
    # 设置初始值
    dp = np.zeros((len(w1) + 1, len(w2) + 1), dtype=int)
    dp[0] = range(len(w2) + 1)
    dp[:, 0] = range(len(w1) + 1)
    # print(dp)

    # 注意下面这个起始值，必须从1开始，否则，可产生不易察觉的bug，因为dp[-1,-1]是存在的合理取值
    for i in range(1, len(w1) + 1):
        for j in range(1, len(w2) + 1):
            if w1[i - 1] == w2[j - 1]:
                dp[i, j] = dp[i - 1, j - 1]
            else:
                dp[i, j] = min(dp[i - 1, j], dp[i, j - 1], dp[i - 1, j - 1]) + 1

    # 打印变更过程
    print(dp)
    # 要从后往前走，最后再从前向后打印，所以下面的string都是加在后面，而不是前面
    # i, j = len(w1), len(w2)
    string = ''
    while i > 0 or j > 0:
        if i > 0 and dp[i, j] == dp[i - 1, j] + 1:
            string = f'delete  w1[{i - 1}] {w1[i - 1]}\n' + string
            i -= 1
        elif j > 0 and dp[i, j] == dp[i, j - 1] + 1:
            string = f'insert  w2[{j - 1}] {w2[j - 1]}\n' + string
            j -= 1
        elif i > 0 and j > 0 and dp[i, j] == dp[i - 1, j - 1] + 1:
            string = f'replace w1[{i - 1}] {w1[i - 1]} with w2[{j - 1}] {w2[j - 1]}\n' + string
            i -= 1
            j -= 1
        else:
            # dp[i, j] == dp[i - 1, j - 1] 的情况
            i -= 1
            j -= 1
    print(string)

    return dp[-1, -1]


if __name__ == '__main__':
    # print(contains('abcde', 'ace'))

    s = Solution()
    # res = s.minDistance('horse', 'ros')
    # res = s.minDistance('axb', 'aybc')
    # res = s.minDistance('a', 'b')
    # res = s.minDistance('intention', 'execution')
    # res = s.minDistance('plasma', 'altruism')

    # 过了995个测试用例，下面这个实在难顶，它可以切分成prosper，ity，最后结果1+3=4
    # res = s.minDistance('prosperity', 'properties')
    # res = s.minDistance('ity', 'ties')

    # 这个没问题了，但下面更长的又会超时
    # res = s.minDistance('abcdxabcde', 'abcdeabcdx')
    # res = s.minDistance('aabcdxabcde', 'abcdeabcdx')

    # 超时，需要加上lru_cache
    res = s.minDistance('dinitrophenylhydrazine', 'acetylphenylhydrazine')

    print(f'递归次数：{count}')
    print(res)

    # print(md('din', 'ac'))
    print(md('intention', 'execution'))
    print(md('plasma', 'altruism'))
    print(md('prosperity', 'properties'))
    print(md('abcdxabcde', 'abcdeabcdx'))
    print(md('aabcdxabcde', 'abcdeabcdx'))
    print(md('dinitrophenylhydrazine', 'acetylphenylhydrazine'))

    print(md('ation', 'tiona'))  # 这种大段相同的情况，在递归矩阵中表现为一段长斜线的相同值
