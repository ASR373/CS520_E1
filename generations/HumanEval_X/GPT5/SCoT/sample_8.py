def max_product_pair(nums: list[int]) -> tuple[int, int]:
    """
    Return the pair of numbers in nums whose product is maximum.
    """
    if len(nums) < 2:
        raise ValueError("Need at least two numbers")
    nums = sorted(nums)
    pair1 = (nums[0], nums[1])
    pair2 = (nums[-1], nums[-2])
    return pair1 if nums[0]*nums[1] > nums[-1]*nums[-2] else pair2