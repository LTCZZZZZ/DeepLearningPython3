# 给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
# 子数组 是数组中的一个连续部分。

class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        # dp[i]表示以num[i]为结尾的子数组的最大和
        # 状态转移方程很简单，如果dp[i-1]为负，则dp[i]=nums[i]，否则等于dp[i-1]+nums[i]
        dp = []
        for i in range(len(nums)):
            if i == 0:
                dp.append(nums[i])
            else:
                if dp[i - 1] < 0:
                    dp.append(nums[i])
                else:
                    dp.append(dp[i - 1] + nums[i])
        return max(dp)


class SolutionDemo:
    def maxSubArray(self, nums: list[int]) -> int:
        res = -float('inf')
        count = 0
        for i in nums:
            count += i
            if count > res:
                res = count
            if count < 0:
                count = 0
        return res
