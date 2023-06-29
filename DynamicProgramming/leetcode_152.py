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
    # 此算法的复杂度较之常规的动态规划要低不少
    s2 = Solution2()
    print(s2.maxProduct([2, -5, -2, -4, 3]))
    print(s2.maxProduct([-2, 0, -1]))
