def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (0-indexed).
    """
    if n < 0:
        raise ValueError("Negative index not allowed")
    if n in (0, 1):
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b