def count_vowels(s: str) -> int:
    """
    Count vowels (a, e, i, o, u) in string s, case-insensitive.
    """
    vowels = set("aeiou")
    return sum(1 for ch in s.lower() if ch in vowels)
