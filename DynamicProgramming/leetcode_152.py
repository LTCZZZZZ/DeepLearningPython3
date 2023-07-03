# 给你一个整数数组 nums，请你找出数组中乘积最大的非空连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。
# 测试用例的答案是一个 32-位 整数。
# 子数组 是数组的连续子序列。

class Solution1:
    def maxProduct(self, nums: list[int]) -> int:
        """
        思路：0将数组分割成多段，每一段独立处理，然后将结果存储在product_list中，最后返回product_list中的最大值，
        对任意不含0的段，从头开始，负数将其分段，
        """
        if len(nums) == 1:
            return nums[0]

        product_list = []
        # 记录每段中不为0的数的个数，用于判断是否需要将product加入product_list
        # 因为有超过1个数时，任意乘积必得至少一个正数（考虑任意相邻2个数，含正数不谈，自己就是，负负得正，证毕）
        # has_posi变量废弃
        count = 0
        product = 1
        temp_product = 1
        # has_posi = False
        has_nega = False
        nega = 1
        for i in nums:
            # print(product, temp_product)
            if i > 0:
                # has_posi = True
                count += 1
                if not has_nega:
                    product = product * i
                else:
                    temp_product = temp_product * i
            elif i == 0:
                product_list.append(0)
                # or product > 1 条件是为了覆盖单段只含一个正数的情况
                if count > 1 or product > 1:
                    product_list.append(max(product, temp_product))
                count = 0
                product = 1
                temp_product = 1
                # has_posi = False
                has_nega = False
                nega = 1
            else:
                count += 1
                if not has_nega:
                    has_nega = True
                    nega = i
                else:
                    # print(product, nega, temp_product, i)
                    product = product * nega * temp_product * i
                    has_nega = False
        if count > 1 or product > 1:
            product_list.append(max(product, temp_product))

        return max(product_list)


class Solution2:
    def maxProduct(self, nums: list[int]) -> int:

        if len(nums) == 1:
            # 特殊处理只含一个负数的情况（只含一个正数时用不到这里）
            return nums[0]

        nums.append(0)  # 在末尾添加0，方便处理，这样可自动结算最后一段数据，这行代码需要上面特殊处理的支持，否则，[-1]会得到结果0

        product_list = []
        start_index = 0
        nega_count = 0
        nega_indexes = []

        for i, num in enumerate(nums):
            if num == 0:
                # 结算前一段的数据
                if i - start_index == 1:
                    # 特殊处理只含一个负数的情况（只含一个正数时用不到这里）
                    product_list.append(nums[start_index])
                elif i > start_index:
                    # 此时表示有数据
                    if nega_count % 2 == 0:
                        product = 1
                        for j in range(start_index, i):
                            product *= nums[j]
                        product_list.append(product)
                    else:
                        # 奇数个负数，等于1和大于1的情况不同
                        if nega_count == 1:
                            # 无公共段落，直接取两边的乘积大者
                            p1 = 1
                            for j in range(start_index, nega_indexes[0]):
                                p1 *= nums[j]
                            p2 = 1
                            for j in range(nega_indexes[-1] + 1, i):
                                p2 *= nums[j]
                            product_list.append(max(p1, p2))
                        else:
                            # 有公共段落，取含两端负数的乘积小者（此时绝对值大）
                            p1 = 1
                            for j in range(start_index, nega_indexes[0] + 1):
                                p1 *= nums[j]
                            p2 = 1
                            for j in range(nega_indexes[-1], i):
                                p2 *= nums[j]
                            p = min(p1, p2)
                            common = 1
                            for j in range(nega_indexes[0] + 1, nega_indexes[-1]):
                                common *= nums[j]
                            product_list.append(p * common)

                product_list.append(0)
                start_index = i + 1
                nega_count = 0
                nega_indexes = []
            else:
                if num < 0:
                    nega_count += 1
                    nega_indexes.append(i)

        return max(product_list)


class Solution3:
    """
    动态规划版，想了想，此算法貌似也适用于数组元素含绝对值小于1的浮点数的情况
    """

    def maxProduct(self, nums: list[int]) -> int:
        # s_max[i]为以nums[i]结尾的连乘积最大值
        # s_min[i]为以nums[i]结尾的连乘积最小值
        s_max = []
        s_min = []
        for i, num in enumerate(nums):
            if i == 0:
                s_max.append(num)
                s_min.append(num)
            else:
                # 简单得想：s_max和s_min的值好像只能从这3个值中产生
                p1 = s_max[i - 1] * num
                p2 = s_min[i - 1] * num
                s_max.append(max(p1, p2, num))
                s_min.append(min(p1, p2, num))
        return max(s_max)


class SolutionDemo:
    """
    这个算法我看了半天没看懂，
    然后我看懂了，算法的原理是基于：
    首先，以0分成若干段，每段的乘积最大值只可能是：必然包含从最左边开始或最右边开始的段，证明如下：
    反证法，对任意不含0的段，若存在某不含端的中间段乘积最大（不考虑元素=1的情况），则此段左1必为负数，否则可将左1加入段，
    同理可知右1必为负数，然而，此时将左1和右1都加入段，段的乘积更大，与假设矛盾，故不存在不含端的中间段乘积最大的情况。

    此算法是从左右两端分别开始，每次计算一步，然后存储最大值，遇到前一段乘积为0时，抛弃前一段，从当前元素开始计算。

    启发性思考："总体"有点守恒的感觉，你思考得越多，算法内包含的默认规则越多，机器就可以更少得运算；
    反之，你思考得越少，算法内蕴含的规则越少，机器要运算得就越多。
    感觉就像，机器通过额外的运算来cover了你没有包含在算法内的规则。

    发散思考：能否构建一个相关的数据结构，来具象化地表示这些，
    比如解决一个问题，总量是100，解法A算法规则占模80，计算机计算占模20，而另一个解法B算法占模60，计算占模40，这样
    """
    def maxProduct(self, nums: list[int]) -> int:
        r_nums = nums[::-1]
        res = nums[0]
        a, b = 1, 1
        for i in range(len(nums)):
            a = a * nums[i] if a else nums[i]
            b = b * r_nums[i] if b else r_nums[i]
            res = max(res, a, b)
        return res


if __name__ == '__main__':
    s1 = Solution1()
    # print(s1.maxProduct([-2, 3, -4]))
    print(s1.maxProduct([2, -5, -2, -4, 3]))  # 经典错误案例
    # 由此案例，知Solution1的思路是错误的，以此为例，运行至i=-4时，product=20，前面3个数字被视为了不可拆分的一整段，
    # 而实际上，此例最大值需[-2,-4,3]，即product=24，Solution1算法没有考虑过这种情况

    # 思考：考虑不含0的段，原为n(n>=2)个正数，任选其中m(m<=n)个变为负数，最大乘积段包含p个负数，则p必为偶数，
    # 若m为偶数，则p=m，取整个段；
    # 若m为奇数，则p<m且p为偶数，显然，由数组的链式结构可知，若p<m-1，则必可找到p'>p，使p'包含p的全部元素，
    # 于是，p必须等于m-1，这时只需比较段的两端（从端向内，到第一个负数为止），取乘积绝对值大者即可，
    # 此算法的复杂度较之常规的动态规划感觉要低不少，但写出Solution3后发现这是我的错觉。。。
    s2 = Solution2()
    print(s2.maxProduct([2, -5, -2, -4, 3]))
    print(s2.maxProduct([-2, 0, -1]))

    s3 = Solution3()
    print(s3.maxProduct([2, -5, -2, -4, 3]))
    print(s3.maxProduct([-2, 0, -1]))

    d = SolutionDemo()
    print(d.maxProduct([2, -5, -2, -4, 3]))
    print(d.maxProduct([-2, 0, -1]))
