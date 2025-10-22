def is_palindrome(s: str) -> bool:
    """
    Return True if the string s is a palindrome, False otherwise.
    """
    s = ''.join(ch.lower() for ch in s if ch.isalnum())
    return s == s[::-1]