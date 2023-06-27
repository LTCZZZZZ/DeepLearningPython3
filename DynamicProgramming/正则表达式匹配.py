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


class m_obj:

    def __init__(self, start, end, string):
        self.start = start
        self.end = end
        self.match = string

    def __str__(self):
        return f'<m_obj object; span=({self.start}, {self.end}), match={self.match}>'

    def __bool__(self):
        return True


# print(m_obj(3, 4, 'ab'))


def exect_match(pattern, string):
    # pattern只含'.'，且长度小于等于string
    signal = 1
    if len(pattern) > len(string):
        signal = 0
    else:
        for i in range(len(pattern)):
            if pattern[i] != '.' and pattern[i] != string[i]:
                signal = 0
                break
    return signal


def d_match(pattern: str, string: str, offset=0):
    # 这个算法中间做了颇多无用功，主要集中在"先取最多个数的字符去匹配"那里，这在string特别长的时候会造成很大的开销
    # 且，关键问题在于，如果从长往短匹配，那么长的可能会优先匹配到某个后位置的，比如start=5，于是结束程序，
    # 但更短的可能会在更前的位置匹配到，比如start=3，于是这个逻辑就有问题了；
    # 从短往长匹配也会有这个问题，就是在某个后的位置先匹配到，所以这个整体逻辑顺序要改
    # 思路是：在string当前位置穷尽所有匹配之前，string禁止向后移位

    # 更优的算法参见KMP算法及后续...
    # print(pattern, string)

    if exect_match(pattern, string):
        return m_obj(offset, offset + len(pattern), string[:len(pattern)])
    else:
        if '*' not in pattern:
            # 全都匹配不到的情况
            if len(pattern) > len(string):
                return None
            # 注意这里的offset，很巧妙
            return d_match(pattern, string[1:], offset=offset + 1)
        else:
            # 此处只需要处理含一个*的情况，含多个*的情况会在递归中自动处理
            count = pattern.count('*')  # 注意到每个*结构至少占2个字符，但它最少的情况下可能匹配0个字符
            index = pattern.index('*')  # 第一个*的索引
            upper = len(string) - len(pattern) + count * 2  # 此*结构至多可匹配的字符数上限
            if upper < 0:
                upper = 0
            # 自然数倒序，取到0。思路是先取最多个数的字符去匹配，比如't*asd'可能取'tttttasd'去匹配，然后依次减少t的个数
            for i in range(upper, -1, -1):
                pat = pattern[:index - 1] + pattern[index - 1] * i + pattern[index + 1:]
                # 注意，这里显然不能直接return d_match(pat, string)
                res = d_match(pat, string)
                if res:
                    return res


N = 0


def d_match1(pattern: str, string: str, offset=0):
    # 此函数体中对string完全不移位（即必从string第一位开始匹配）
    # print(pattern, string)
    # global N
    # N += 1

    if exect_match(pattern, string):
        return m_obj(offset, offset + len(pattern), string[:len(pattern)])
    else:
        if '*' not in pattern:
            # 因为在主函数中验证过exect_match，所以这里直接返回None
            return None
        else:
            # 此处只需要处理含一个*的情况，含多个*的情况会在递归中自动处理
            count = pattern.count('*')  # 注意到每个*结构至少占2个字符，但它最少的情况下可能匹配0个字符
            index = pattern.index('*')  # 第一个*的索引
            upper = len(string) - len(pattern) + count * 2  # 此*结构至多可匹配的字符数上限
            if upper < 0:
                upper = 0
            # 自然数倒序，取到0。思路是先取最多个数的字符去匹配，比如't*asd'可能取'tttttasd'去匹配，然后依次减少t的个数
            for i in range(upper, -1, -1):
                pat = pattern[:index - 1] + pattern[index - 1] * i + pattern[index + 1:]
                # 注意，这里显然不能直接return d_match(pat, string)
                res = d_match1(pat, string, offset)
                if res:
                    return res


def d_match2(pattern: str, string: str, offset=0):
    # 改进版，此函数看着感觉没问题了，通过了下方所有的用例测试，
    # 就是匹配时有大量无用的计算，即贪婪时哪怕没匹配到一个字符，也会从最贪婪开始匹配，导致递归次数非常多
    # 此外，如果string本身很长，由于算法内采用了upper变量，由代码逻辑可知此函数将占用大量的时间和空间复杂度，应该是效率极低的算法
    # print(pattern, string, offset)

    res = d_match1(pattern, string, offset)
    if res:
        return res
    else:
        # 确保待匹配的串长度要大于0
        if len(string[1:]) > 0:
            # 注意这里是d_match2而不是d_match1，如果是d_match1，那么递归只会进行到string[1:]就停住了
            return d_match2(pattern, string[1:], offset=offset + 1)
        else:
            return None


def re_match(pattern: str, string: str, offset=0):
    # d_match优化为尽量和re.search效果相同的版本
    # print(pattern, string)

    if exect_match(pattern, string):
        return m_obj(offset, offset + len(pattern), string[:len(pattern)])
    else:
        if '*' not in pattern:
            # 全都匹配不到的情况
            if len(pattern) > len(string):
                return None
            # 注意这里的offset，很巧妙
            return re_match(pattern, string[1:], offset=offset + 1)
        else:
            # 此处只需要处理含一个*的情况，含多个*的情况会在递归中自动处理
            count = pattern.count('*')  # 注意到每个*结构至少占2个字符，但它最少的情况下可能匹配0个字符
            index = pattern.index('*')  # 第一个*的索引
            upper = len(string) - len(pattern) + count * 2  # 此*结构至多可匹配的字符数上限
            if upper < 0:
                upper = 0
            # print('upper: ', upper)
            # 因为是贪婪模式，所以't*asd'假如取'tasd'匹配到之后，在"同样的位置"还要尝试'ttasd'
            for i in range(0, upper + 1):
                pat = pattern[:index - 1] + pattern[index - 1] * i + pattern[index + 1:]
                # 注意，这里显然不能直接return d_match(pat, string)
                # 算法在这个位置仍然做了很多无用功，因为本来首字母匹配不到string就该往后跳的，但此处会尝试先替换完全部的*
                res = re_match(pat, string)
                if res:
                    for j in range(i + 1, upper + 1):
                        pat = pattern[:index - 1] + pattern[index - 1] * j + pattern[index + 1:]
                        res2 = re_match(pat, string)
                        # print(j)
                        # print(pat, string)
                        # print(res2)
                        # 匹配到了但匹配的位置偏后，或者没匹配到
                        # （特别注意：由于算法的冗余操作，这里没匹配到，不代表j更大时也匹配不到，
                        # 只不过j更大时即使能匹配到，匹配到的位置也必定在res.start之后，所以不予考虑）
                        if res2 and res2.start > res.start or res2 is None:
                            return res
                        # print(res2)
                        # 在匹配到且res2.start = res.start时会自动进入下一个循环
                    # 如果循环完了还没return，此时return res2
                    return res2


# 测试组
print('re_match:', re_match('st*asd', 'sttasdkjlstasd'))  # 如果拿替换*后的去匹配整个字符串，则这类匹配很容易出问题(无论替换次数是从多到少还是从少到多)
print('d_match2:', d_match2('st*asd', 'sttasdkjlstasd'))
print(re.search('st*asd', 'sttasdkjlstasd'))

# 注意：下面的注释"匹配不到"和"匹配错误"是两码事，匹配不到表示正常就匹配不到，匹配错误表示程序本身有问题

# print(single_match('.jd.a', 'skfljdtalkfj'))
# print(match('.jd.a', 'skfljdtalkfj'))
print('d_match2:', d_match2('.jd.a', 'skfljdtalkfj'))
print(re.search('.jd.a', 'skfljdtalkfj'))
# print(single_match('.jdkf', 'skfljdtalkfj'))
# print(match('.jdkf', 'skfljdtalkfj'))
print('d_match2: ', d_match2('.jdkf', 'skfljdtalkfj'))
print(re.search('.jdkf', 'skfljdtalkfj'))
# print(single_match('.jd.*a', 'skfljdtalkfj'))
print('_____________________________________')


# print(match('.jdt*a', 'skfljdtttalkfj'))
# print(d_match('.jdt*a', 'skfljdtttalkfj'))
# print(re_match('.jdt*a', 'skfljdtttalkfj'))
print('d_match2:', d_match2('.jdt*a', 'skfljdtttalkfj'))
print(re.search('.jdt*a', 'skfljdtttalkfj'))

# print(match('.jdt*ta', 'skfljdtttalkfj'))  # 匹配错误，好像会进入无限循环
# print(d_match('.jdt*ta', 'skfljdtttalkfj'))  # 匹配成功
# print(re_match('.jdt*ta', 'skfljdtttalkfj'))  # 匹配成功
print('d_match2:', d_match2('.jdt*ta', 'skfljdtttalkfj'))
print(re.search('.jdt*ta', 'skfljdtttalkfj'))
print('_____________________________________')

# print(match('.jd.*a', 'skfljdtalkfj'))  # 匹配错误
# print(d_match('.jd.*a', 'skfljdtalkfj'))  # 匹配成功
# print(re_match('.jd.*a', 'skfljdtalkfj'))  # 匹配成功
print('d_match2:', d_match2('.jd.*a', 'skfljdtalkfj'))
print(re.search('.jd.*a', 'skfljdtalkfj'))

# print(match('.jd.*', 'skfljdtalkfj'))
# print(d_match('.jd.*', 'skfljdtalkfj'))
# print(re_match('.jd.*', 'skfljdtalkfj'))
print('d_match2:', d_match2('.jd.*', 'skfljdtalkfj'))
print(re.search('.jd.*', 'skfljdtalkfj'))

print('_____________________________________')
# 匹配成功
# print(d_match('.f*k*h*e*', 'asdfffkkgheeeokj'))
# print(re_match('.f*k*h*e*', 'asdfffkkgheeeokj'))
print('d_match2:', d_match2('.f*k*h*e*', 'asdfffkkgheeeokj'))
print(re.search('.f*k*h*e*', 'asdfffkkgheeeokj'))
print()

# print(d_match('f*k*h*e*', 'asdfffkkheeeokj'))
# print(re_match('f*k*h*e*', 'asdfffkkheeeokj'))
print('d_match2:', d_match2('f*k*h*e*', 'asdfffkkheeeokj'))
print(re.search('f*k*h*e*', 'asdfffkkheeeokj'))
print()

print('_____________________________________')
# 注意这个例子，很经典
# print('d_match:', d_match('fk*h*e*', 'asdfffkkheeeokj'))  # 匹配成功，但和re匹配的结果不同，fkkheee
print('d_match2:', d_match2('fk*h*e*', 'asdfffkkheeeokj'))
# print('N:', N)  # 上面那个递归了2511次，有大量无用的计算
# print('re_match', re_match('fk*h*e*', 'asdfffkkheeeokj'))  # 匹配成功，且结果相同
print(re.search('fk*h*e*', 'asdfffkkheeeokj'))  # 有多个成功的匹配，re只取了第一个，f
print(re.findall('fk*h*e*', 'asdfffkkheeeokj'))  # 有多个成功的匹配，findall取不重叠的，['f', 'f', 'fkkheee']
print()

print('_____________________________________')
# print(d_match('fk*h*e*', 'asdfkkheeeokj'))
print(d_match2('fk*h*e*', 'asdfkkheeeokj'))
# print(re_match('fk*h*e*', 'asdfkkheeeokj'))  # 匹配成功，但和re匹配的结果不同，f
print(re.search('fk*h*e*', 'asdfkkheeeokj'))

# 基本已经完善，但还差在含(.*)结构或特殊情况时从后往前检索的问题，见程序运行的结果
# 但即使完善了，这种控制流的方式既看起来复杂又容易出错，中间还有部分重复计算的地方。
# 注意，需要考虑诸如 (.*h*)这种结构，感觉有点复杂
# 用动态编程的思想再搞一遍
