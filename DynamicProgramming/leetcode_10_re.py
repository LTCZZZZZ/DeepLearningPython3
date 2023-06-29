# leetcode 的第 10 号题
# 给你一个字符串s和一个字符规律p，请你来实现一个支持 '.'和'*'的正则表达式匹配。
# '.' 匹配任意单个字符
# '*' 匹配零个或多个前面的那一个元素
# 所谓匹配，是要涵盖整个字符串s的，而不是部分字符串。
import re
import time


def simplify(pattern):
    # 将pattern中连续的诸如'a*a*'的结构合并为一个

    length = len(pattern)
    i = 0
    while i < length:
        if pattern[i] == '*':
            # 我们默认表达式是正确的，所以pattern[i-1]一定存在
            char = pattern[i - 1]
            # 注意这里用的是while不是if，因为可能有'a*a*a*'这种情况
            while i + 2 < length and pattern[i + 1:i + 3] == char + '*':
                pattern = pattern[:i + 1] + pattern[i + 3:]
                length -= 2
        i += 1
    return pattern


def exect_match(pattern, string):
    # pattern只含'.'
    l = len(pattern)
    signal = 1
    if l != len(string):
        signal = 0
    else:
        for i in range(l):
            if pattern[i] != '.' and pattern[i] != string[i]:
                signal = 0
                break
    return signal


N = 0


def d_match1(pattern: str, string: str):
    # print(pattern, string)
    # global N
    # N += 1
    # if N % 100000 == 0:
    #     print(N)
    #     print(pattern, string)

    if exect_match(pattern, string):
        return True
    else:
        if '*' not in pattern:
            return False
        else:
            count = pattern.count('*')
            index = pattern.index('*')
            # 先比较pattern[:index-1]和string[:index-1]
            if not exect_match(pattern[:index - 1], string[:index - 1]):
                return False
            upper = len(string) - len(pattern) + count * 2
            if upper < 0:
                upper = 0
            for i in range(upper + 1):
                pat = pattern[:index - 1] + pattern[index - 1] * i + pattern[index + 1:]
                res = d_match1(pat, string)
                if res:
                    return res
    return False


class Solution:

    def isMatch(self, s: str, p: str) -> bool:
        p = simplify(p)
        print(p)
        res = d_match1(p, s)
        return res


time1 = time.time()
s = Solution()
print(s.isMatch("aaaaaaaaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*a*"))
print(N)
print('time:', time.time() - time1)

# m = re.search('(a*)(a*)a*a*a*a*a*a*a*a*b', 'aaaaaaaaaaaaaaaaaaab')
# print(m)
# print(m.groups())
