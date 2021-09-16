# 给你一个字符串 string 和一个字符规律 pattern，实现一个支持 '.' 和 '*' 的正则表达式匹配
# '.' 匹配任意单个字符，'*' 匹配零个或多个前面的那一个元素

import re
import time


def single_match(pattern, string):
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


def match0(pattern, string):
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


# 有问题的版本，在含(.*)结构或特殊情况时没有从后往前检索，
# 其实应该是贪婪逐一吐出，见match函数注释
def match1(pattern, string):
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
                # 注意，j + 1 < len(pattern)的情况下才能取到pattern[j + 1]
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


# 当贪婪模式尽可能贪婪的匹配到时，如果最终匹配失败，要从之前的贪婪中逐一吐出字符，再进行匹配
# 如果不用DynamicProgramming，相当于每次遇到一个贪婪模式，就要新起一个变量记录匹配情况以便于回溯，
# 故此这需要用一个列表来记录，一旦全局匹配失败，列表中元素从后往前，逐次减一至0，
# 比如三个贪婪依次匹配了[5,3,2]个字符，要先[5,3,1]往后，[5,3,0]往后，[5,2]往后，这样下去，最终到[0]往后，
# 这个列表是一个不断增长变短的(对象)，比如，它可能[5,3,1]→[5,3,1,3]→[5,2]这样
def match(pattern, string):
    # 此循环与上面不同，string在外层，pattern在内层
    # 支持 '.' 和 '*'

    # res, j, m_i 表示当前匹配到的状态，首先抽象出一个输入此三个参数输出匹配结果的函数
    def in_out(res, j, m_i, greed_list):
        signal = 0  # 是否匹配成功的标志位

        greed_match = 0
        while True:
            # print(j, m_i)
            # pattern耗尽，匹配成功；或者string耗尽且pattern最后为贪婪模式且耗到了倒数第二位
            if j == len(pattern) or m_i == len(string) and j == (len(pattern) - 2) and pattern[-1] == '*':
                signal = 1
                break
            # 在pattern耗尽之前，string就已耗尽，匹配不成功
            if m_i == len(string):
                break

            # 上一轮循环是贪婪匹配且匹配成功时，本次循环跳过验证 是否为贪婪模式 这一步。否则都进行验证
            if greed_match:
                greed = 1
            else:
                greed = 0
                # 先判定后一字符是否为 '*'
                if j + 1 < len(pattern) and pattern[j + 1] == '*':
                    # 注意，j + 1 < len(pattern)的情况下才能取到pattern[j + 1]
                    greed = 1
                    greed_list.append(0)

            # print(j, m_i, greed)
            if pattern[j] == '.' or pattern[j] == string[m_i]:
                res.append(string[m_i])
                m_i += 1
                if greed:
                    greed_match = 1
                    greed_list[-1] += 1
                    continue
                else:
                    # 此字符匹配到，且为非贪婪模式
                    j += 1
                    continue
            else:
                if greed:
                    j += 2
                    greed_match = 0
                    # 此时 '*' 和他前面的字符一起匹配0个字符
                    continue
                else:
                    # 字符也没匹配到，字符后也不带 '*'
                    break

        if signal:
            return True, res
        else:
            return False, (res, greed_list)

    i = 0
    while True:
        ok = False  # 从i位置开始是否匹配成功的标志位

        greed_list = []
        # 这里还需要记录贪婪对应的匹配状况，包括pattern和string行进到的位置

        res = []
        j = 0
        m_i = i  # m_i表示pattern已匹配到的序号，初始化的值为i

        # 已尝试完所有匹配，均不成功
        if i == len(string):
            break

        while True:
            ok, res = in_out(res, j, m_i, greed_list)
            if ok:
                break
            else:
                res, greed_list = res
                print(greed_list)
                time.sleep(1)
                # 除非贪婪列表全为0，否则需要向前回溯
                if sum(greed_list) == 0:
                    break
                else:
                    # 更新res, j, m_i
                    pass

        # 匹配成功，直接输出结果
        if ok:
            break
        else:
            # 从位置i起的匹配失败，i自加，然后进入下一次循环
            i += 1

    if ok:
        res = ''.join(res)
    else:
        res = None
    return res


def d_match(pattern, string):
    pass


# print(single_match('.jd.a', 'skfljdtalkfj'))
# print(match('.jd.a', 'skfljdtalkfj'))
# print(single_match('.jdkf', 'skfljdtalkfj'))
# print(match('.jdkf', 'skfljdtalkfj'))
# print(single_match('.jd.*a', 'skfljdtalkfj'))


print(match('.jdt*a', 'skfljdtttalkfj'))
print(re.search('.jdt*a', 'skfljdtttalkfj'))
print(match('.jdt*ta', 'skfljdtttalkfj'))  # 匹配失败
print(re.search('.jdt*ta', 'skfljdtttalkfj'))

print(match('.jd.*a', 'skfljdtalkfj'))  # 匹配失败
print(re.search('.jd.*a', 'skfljdtalkfj'))
print(match('.jd.*', 'skfljdtalkfj'))
print(re.search('.jd.*', 'skfljdtalkfj'))

# 匹配成功
# print(match('.f*k*h*e*', 'asdfffkkgheeeokj'))
# print(re.search('.f*k*h*e*', 'asdfffkkgheeeokj'))
# print(match('f*k*h*e*', 'asdfffkkheeeokj'))
# print(re.search('f*k*h*e*', 'asdfffkkheeeokj'))
# print(match('fk*h*e*', 'asdfffkkheeeokj'))
# print(re.search('fk*h*e*', 'asdfffkkheeeokj'))
# print(match('fk*h*e*', 'asdfkkheeeokj'))
# print(re.search('fk*h*e*', 'asdfkkheeeokj'))

# 基本已经完善，但还差在含(.*)结构或特殊情况时从后往前检索的问题，见程序运行的结果
# 但即使完善了，这种控制流的方式既看起来复杂又容易出错，中间还有部分重复计算的地方。
# 注意，需要考虑诸如 (.*h*)这种结构，感觉有点复杂
# 用动态编程的思想再搞一遍
