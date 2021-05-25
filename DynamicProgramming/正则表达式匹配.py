# 给你一个字符串 string 和一个字符规律 pattern，实现一个支持 '.' 和 '*' 的正则表达式匹配
# '.' 匹配任意单个字符，'*' 匹配零个或多个前面的那一个元素

import re


def single_match(string, pattern):
    # 同样是有问题的版本，会跨字符匹配（间隔匹配）
    # 单字符匹配，支持 '.' 但不支持 '*'
    res = []
    for i in range(len(pattern)):
        # print(string)
        for j in range(len(string)):
            if pattern[i] == '.' or pattern[i] == string[j]:
                res.append(string[j])
                string = string[j + 1:]
                break
    res = ''.join(res)
    return res


def match0(string, pattern):
    # 有问题的版本，'*' 只匹配1到n，没匹配0，另外，存在间隔匹配的情况
    # 支持 '.' 和 '*'
    res = []
    jump_signal = 0
    for i in range(len(pattern)):
        # print(jump_signal)
        # print(string)
        if jump_signal:
            jump_signal = 0
            continue
        signal = 0
        for j in range(len(string)):
            if pattern[i] == '.' or pattern[i] == string[j]:
                # 注意，i + 1 < len(pattern)的情况下才能取到pattern[i + 1]
                res.append(string[j])
                signal = 1
                if i + 1 < len(pattern) and pattern[i + 1] == '*':
                    jump_signal = 1
                    signal = 0  # 在跳入下一次循环前将signal置为0
                    continue
                else:
                    break
        if signal:
            string = string[j + 1:]
    res = ''.join(res)
    return res


def match(string, pattern):
    # 此循环与上面不同，string在外层，pattern在内层
    # 支持 '.' 和 '*'
    i = 0
    while True:

        # 已尝试完所有匹配，均不成功
        if i == len(string):
            break

        res = []
        signal = 0  # 是否匹配成功的标志位
        j = 0
        m_i = i  # m_i表示pattern已匹配到的序号，初始化的值为i
        while True:
            # print(j, m_i)
            # pattern耗尽，匹配成功；或者string耗尽且pattern最后为贪婪模式且耗到了倒数第二位
            if j == len(pattern) or m_i == len(string) and j == (len(pattern) - 2) and pattern[-1] == '*':
                signal = 1
                break
            # 在pattern耗尽之前，string就已耗尽，匹配不成功
            if m_i == len(string):
                break
            # 先判定后一字符是否为 '*'，在continue的情况下，此值实际被计算了多次
            greed = 0
            if j + 1 < len(pattern) and pattern[j + 1] == '*':
                # 注意，i + 1 < len(pattern)的情况下才能取到pattern[i + 1]
                greed = 1

            if pattern[j] == '.' or pattern[j] == string[m_i]:
                res.append(string[m_i])
                m_i += 1
                if greed:
                    continue
                else:
                    # 此字符匹配到，且为非贪婪模式
                    j += 1
                    continue
            else:
                if greed:
                    j += 2
                    # 此时 '*' 和他前面的字符一起匹配0个字符
                    continue
                else:
                    # 字符也没匹配到，字符后也不带 '*'
                    break
        # 匹配成功，直接输出结果
        if signal:
            break
        else:
            # 从位置i起的匹配失败，i自加，然后进入下一次循环
            i += 1
    if signal:
        res = ''.join(res)
    else:
        res = None
    return res


# print(single_match('skfljdtalkfj', '.jd.a'))
# print(match('skfljdtalkfj', '.jd.a'))
# print(single_match('skfljdtalkfj', '.jdkf'))
# print(match('skfljdtalkfj', '.jdkf'))
# print(single_match('skfljdtalkfj', '.jd.*a'))

print(match('skfljdtttalkfj', '.jdt*a'))
print(re.search('.jdt*a', 'skfljdtttalkfj'))
print(match('skfljdtttalkfj', '.jdt*ta'))
print(re.search('.jdt*ta', 'skfljdtttalkfj'))

print(match('skfljdtalkfj', '.jd.*a'))
print(re.search('.jd.*a', 'skfljdtalkfj'))
print(match('skfljdtalkfj', '.jd.*'))
print(re.search('.jd.*', 'skfljdtalkfj'))

# print(single_match('asdfffkkgheeeokj', '.f*k*h*e*'))
# print(match('asdfffkkgheeeokj', '.f*k*h*e*'))
# print(re.search('.f*k*h*e*', 'asdfffkkgheeeokj'))
# print(match('asdfffkkheeeokj', 'f*k*h*e*'))
# print(re.search('f*k*h*e*', 'asdfffkkheeeokj'))
# print(match('asdfffkkheeeokj', 'fk*h*e*'))
# print(re.search('fk*h*e*', 'asdfffkkheeeokj'))
# print(match('asdfkkheeeokj', 'fk*h*e*'))
# print(re.search('fk*h*e*', 'asdfkkheeeokj'))

# 基本已经完善，但还差在含(.*)结构或特殊情况时从后往前检索的问题，见程序运行的结果
# 但即使完善了，这种控制流的方式既看起来复杂又容易出错，中间还有部分重复计算的地方。
# 注意，需要考虑诸如 (.*h*)这种结构，感觉有点复杂
# 用动态编程的思想再搞一遍
