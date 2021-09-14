def table(pattern):
    """对pattern建立辅助表格，数据结构内层是字典，外层是列表，
    千万不要以为辅助表格若除t[i][v]的位置全部以0填充，则此算法就类似于纯暴力算法Brute force了，
    这是错误的，这两种算法有本质的不同，在KMP中，建立辅助表格后，string是永远只从前向后读取一遍，绝不回头的，
    而纯暴力算法Brute force，从string第1位向后匹配，不得，回到第2位，依次类推，string可能会读取很多遍"""

    # t = [{}] * len(pattern)  # 万万没想到这种方式出来的t里面的字典竟然是同一引用对象，，只能换一种方式了

    t = []

    # 填充其他位置，逻辑清晰但效率不怎么样的算法
    # for i in range(len(pattern)):
    #     t.append({pattern[i]: i + 1})
    #     for v in set(pattern[:i]):  # 只用对pattern[i]之前出现过的字符串添加值，其他不添加自动视为0
    #         if v != pattern[i]:  # 只对不匹配的字符设置值
    #             for k in range(i, 0, -1):  # 其实这里k本应取到0，但为0的添加上无意义，如此range的第二个参数设为0而不是-1
    #                 print(i, v, k, pattern[:k], pattern[i - k + 1:i] + v)  # 这一行打印一加，逻辑清晰明了
    #                 # 这个其实就相当于，当不匹配时，即v != pattern[i]时，用v替换掉pattern[i]的位置，
    #                 # 然后依次左移1位，2位...来和pattern比较，看位置对应的部分是否相同
    #                 if pattern[:k] == pattern[i - k + 1:i] + v:
    #                     t[i][v] = k
    #                     break

    # 填充其他位置，较为高效的算法
    # 看了下面这个算法，再看上面那个，简直不堪入目，脸红
    # 这个算法的基本思想是，当v是非匹配字符串时，它对应的值必然和前面某状态x时相同
    x = 0
    for i in range(len(pattern)):
        t.append({pattern[i]: i + 1})  # 匹配的字符
        for v in set(pattern[:i]):  # 只用对pattern[i]之前出现过的字符串添加值，其他不添加自动视为0
            if v != pattern[i]:
                t[i][v] = t[x].get(v, 0)
                # 更新x
                x = t[x].get(pattern[i], 0)

    print(t)
    return t


def KMP(pattern, string):
    """非正则匹配。固定字符串匹配的优化算法(对比于Brute force)，时间复杂度为O(m+n)
    这个过程中指向被匹配字符串的指针并没有发生过回退，我们是通过状态的转换来
    决定接下来应该从模式字符串的哪一个字符开始与被匹配串的下一个字符进行匹配"""
    t = table(pattern)
    i = 0
    j = 0
    while i < len(t):
        try:
            i = t[i].get(string[j], 0)
            j += 1  # 在已建辅助表格的情况下，j是永不回头的
        except IndexError:
            # break
            return False, j
    return True, j, string[j - i:j]


print(KMP('ABABAC', 'AABACAABABACAA'))
