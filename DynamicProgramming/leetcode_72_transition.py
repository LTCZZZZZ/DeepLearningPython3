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

# 初步思路是，让word1包含word2，最后执行删除操作。
# 于是，先找出word1中的word2最大子列，然后对word1扩充(插入，替换)，使之包含word2，最后删除多余的字符。
# 最大子列好像不靠谱啊，比如在上述例子中，rs也是最大子列，但按rs来操作的话，次数就增加了，如果再对相同长度的子列分情况讨论优先级，就太复杂了。
# 改为下面的方式，有个主次之分，以目标字符串word2为主

import numpy as np


def assist(word1, word2):
    """
    从word2中第一个字符开始遍历，每个字符生成一个结果，规则如下：
    设字符为c，如果c不在word1中，生成空字符串或忽略此结果，若在word1中，则从c往后，依次判断word2的剩余字符是否"依序"在word1中，并拿到这个序列
    """
    res = []
    for i, c in enumerate(word2):
        # 每次循环开始时重置初始值（j是word1相关的参数，相当于每次循环都会检视整个word1）
        common = []
        j = 0
        # 注意这两个循环的主体都是word2相关
        is_start = 1
        start_j = -1
        end_j = -1
        end_k = -1
        # print('______________')
        # print(i, c)
        for k, p in enumerate(word2[i:]):
            # print(j, word1[j:], k, p)
            if p in word1[j:]:
                current_index = word1[j:].index(p)

                # 记录word1中最初匹配到的位置
                if is_start == 1:
                    start_j = current_index + j
                is_start = 0

                # 分别记录最后匹配到的位置，注意这里要加j，而下面end_k同样要加i
                end_j = current_index + j
                # print(p, end_j)
                end_k = k + i

                common.append(p)
                # 重新设置j的值，注意这里要加1，因为索引位的值已经被用掉了
                j = current_index + j + 1
            else:
                # 遇到全没搜索到的，可以两者同时向后跳过一个字符（此字符就可用替换操作轻松代替）
                # 但如果是第一个字符c就没搜索到，此时break跳出内层循环直接进入外层的下一个循环
                if is_start:
                    break
                j += 1
                continue
        if common:
            common = ''.join(common)
            # 后4个元素分别是：word1匹配的起始和结束位置，word2匹配的起始和结束位置
            res.append((common, start_j, end_j, i, end_k))

    return res


def contains(w1, w2):
    """
    w1是否按序包含w2，如abcde包含ace
    """

    # w2放在前面，可兼容w1和w2同时耗尽的情况
    if w2 == '':
        return True
    if w1 == '':
        return False

    if w1[0] == w2[0]:
        return contains(w1[1:], w2[1:])
    else:
        return contains(w1[1:], w2)


def assist2(common, word1):
    """
    从word1中找出最紧凑的common
    """
    index_list = []
    for i, c in enumerate(word1):
        if common[0] == c:
            index_list.append(i)

    res = []
    for ix in index_list:
        if contains(word1[ix:], common):
            res.append(ix)
    return max(res)


def md(word1: str, word2: str) -> int:
    common_list = assist(word1, word2)
    print(common_list)
    lengths = [len(v[0]) for v in common_list]
    if len(lengths) == 0:
        res = max(len(word1), len(word2))
    else:
        index = np.argmax(lengths)
        # index = lengths.index(max(lengths))
        item = common_list[index]
        item = list(item)
        item[1] = assist2(item[0], word1)
        print(item)
        res = max(item[1], item[3]) + ((item[2] - item[1] + 1) - (len(item[0]))) + \
              max((len(word1) - 1 - item[2]), (len(word2) - 1 - item[4]))
        res = min(res, max(len(word1), len(word2)))
    return res


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        return min(md(word1, word2), md(word2, word1))


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

    # 下面这个用例就直接挂掉了，没办法
    res = s.minDistance('abcdxabcde', 'abcdeabcdx')

    print(res)
