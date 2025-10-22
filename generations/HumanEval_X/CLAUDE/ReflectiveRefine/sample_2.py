def factorial(n: int) -> int:
    """
    Compute n! for non-negative integer n.
    """
    if n < 0:
        raise ValueError("Negative input not allowed")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result