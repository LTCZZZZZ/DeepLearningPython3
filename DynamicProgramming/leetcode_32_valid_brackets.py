# leetcode 的第 32 号题：最长有效括号
# 给你一个只包含 '(' 和 ')' 的字符串，找出最长有效（格式正确且连续）括号子串的长度。

# 此题的dp算法太麻烦了，而且逻辑极易出错，就不写了
# （因为下面的简高算法是我自己想出来的，就偷个懒，如果一个解决方案都没想出来，那还是要写一下）


# def valid_brackets(s: str):
#     signal = 0
#     left = 0
#     right = 0
#     count_list = []
#     for c in s:
#         if c == '(':
#             left += 1
#             signal += 1
#         else:
#             signal -= 1
#             right += 1
#             if signal >= 0:
#                 count_list.append(right)
#
#         if signal == 0:
#             count_list.append(left)
#             # 注意这时要重置right但不重置left
#             right = 0
#         elif signal < 0:
#             signal = 0
#             left = 0
#             right = 0
#
#     print(count_list)
#     if len(count_list) == 0:
#         return 0
#     return max(count_list) * 2


def valid_brackets(s: str):
    """
    定义辅助函数之后，正面来一遍，以'('计数，然后反面来一遍，以')'计数
    这个思维很巧妙，从左向右搜索时，多出来的右括号必然为非法字符，同理，从右向左搜索时，多出的左括号必为非法字符
    于是，在从左向右扫过字符串时，就无需考虑子串中左括号数大于右括号而子串的子串为合法序列的情况，它会在从右向左扫描时自动添加，
    例如(()(((()，正向扫描时(()为尚可以向后扫描的未出错子串，()为子串的合法子串，但此时无需考虑它。

    时间复杂度O(n)
    空间复杂度O(1)
    此算法十分优秀
    """

    def assist(s: str, char: str):
        signal = 0
        count = 0
        count_list = []
        for c in s:
            if c == char:
                count += 1
                signal += 1
            else:
                signal -= 1

            if signal == 0:
                count_list.append(count)
            elif signal < 0:
                signal = 0
                count = 0

        print(count_list)
        if len(count_list) == 0:
            return 0
        return max(count_list) * 2

    return max(assist(s, '('), assist(s[::-1], ')'))


if __name__ == '__main__':
    valid_brackets('(()')
    valid_brackets(')()())')
    valid_brackets('(()(((()')

