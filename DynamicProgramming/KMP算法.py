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
    # x表示的是当下一个吃进字符造成不匹配时，当前已匹配串的最长可匹配子串的长度（从当前位置向左数x然后切开）
    # x也是不断动态更新的，可增大可减小

    # 可这么看，每次循环中，更新前x为pattern[:i]与自己向左任意移位(至少1位)后的最大匹配长度，
    # 换一种说法就是，前缀和后缀相同的最大长度！！！！！！！！！！！！！！！！！！
    # 更新后x为pattern[:i+1]与自己向左任意移位(至少1位)后的最大匹配长度，
    # 以ABABAC为例：
    # i=0时不考虑
    # i=1时pattern[:i]='A'，移位就没了，故x=0
    # i=2时pattern[:i]='AB'，向左任意移位后都无法匹配，故x=0
    # i=3时pattern[:i]='ABA'，向左移2位后匹配A，故x=1
    # i=4时pattern[:i]='ABAB'，向左移2位后匹配AB，故x=2
    # i=5时pattern[:i]='ABABA'，向左移2位后匹配ABA，故x=3
    # i=6时pattern[:i]='ABABAC'，向左任意移位后都无法匹配，故x=0
    # 至于x更新的原理，考虑pattern[:i+1]与自己的真子串的匹配情况，正如用pattern去匹配string一样，
    # 可以从pattern[:i]已建立的辅助表格及真子串的当前匹配情况x得出，即x = t[x].get(pattern[i], 0)
    # 于是可以复用之前的结果，这个算法细思起来当真巧妙，抽象到了如此程度，我简直要拍案叫绝
    # 又，可以如此思考：待匹配字符串可视为输入流，因为它是不回退的，table视为一个状态机，它根据输入流的输入改变并输出当前状态
    # x即可以视为将pattern的第一个字符去掉后的输入流输入table得到的匹配状态，
    # table这个状态机在构建的过程中不断利用自身

    x = 0
    for i in range(len(pattern)):
        t.append({pattern[i]: i + 1})  # 匹配的字符
        if i > 0:
            for v in set(pattern[:i]):  # 只用对pattern[i]之前出现过的字符串添加值，其他不添加自动视为0
                if v != pattern[i]:
                    t[i][v] = t[x].get(v, 0)
            print('更新前：', i, x)
            # 更新x
            x = t[x].get(pattern[i], 0)
            # print('更新后：', i, x)
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


# 另一种更自然的思想，算法应该是源于这种思想，由此可知，KMP算法相当于是缩短了暴力算法Brute force中的某些过程
# 仔细观察这张图就能发现，这样非常低效，我们能够直观地看到模式串除了第一个是B之外其他的位置上的字母都是A，
# 在位置六失配，所以前面一段必然全是A，我们直接把模式串的起始端移动到六位置就可以了，前面的一步一步移动的操作是可以跳过的，
# 基于这一现象，深入思考，我们可以发现，根据模式串的情况，我们可以推断出来当在某个位置出现失配的时候我们应该怎么去移动模式串,
# 为什么呢？因为当在六位置失配的时候，我们已经知道了第六位之前的五位是匹配的，当我们将模式串向前移动一位再进行匹配的时候，
# 相当于让模式串跟去掉第一个字符并左移一位的自己进行匹配(严格来说不是自己，是自己的一个去掉第一个字符并左移一位的自己的前缀)，
# 失配后再重复这个过程。既然是跟自己的一部分匹配，那我们可以在模式串自身进行这个过程并记录下来各种情况出现的时候该怎么移动，
# 那么，我们就需要构造一个有限状态自动机了。

# 我们现在要做的事情是这样的，首先用一个指针x指向0状态，然后我们可以直接把0状态里的数值直接拷贝到1状态，
# 因为当在一状态的时候发生不匹配的时候，我们会用已匹配串的去掉首字母前缀进行匹配，结果是空的，因为此时就一个字母匹配，
# 然后我们再用不匹配的那个字母跟模式字符串的第一个字母去匹配，得到模式应该处于的状态，
# 所以可以直接将第一个字母的对应的状态机的这一列拷贝过来，直接拿到结果。
# 然后这个过程是迭代的，也就是说，当我们在模式串的第三个字符失配的时候，我们实际上是在拿模式串的第二个字符(因为模式串这时
# 肯定要向前进一)去跟模式串的0状态匹配，然后得到我们用来进行匹配的下一个状态，我们已经通过x = dfa[pat.charAt(j)][x]
# 得到了输入模式串的第二个字符后自动机的状态，也就是说x现在指向的那一列状态就是当前待匹配字符输入之后应该转换到的状态了
# (也就是说，在当前位置失配了，当前位置的文本串应该去跟x位置的模式串字符去做匹配)，所以我们可以把x指向的那一列直接抄过来。
# 匹配进状态进一，不匹配把去掉首字母已匹配串的的前缀输入状态机(这个操作在构造状态机的过程中迭代进行，没有重复操作)，
# 这样一个状态机就构造出来了。

# 链接：https://www.jianshu.com/p/18410598c061
