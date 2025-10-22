def sum_of_squares(nums: list[int]) -> int:
    """
    Return the sum of squares of all numbers in nums.
    """
    return sum(x * x for x in nums)