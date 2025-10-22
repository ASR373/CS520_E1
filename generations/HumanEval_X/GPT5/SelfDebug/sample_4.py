def reverse_words(text: str) -> str:
    """
    Reverse order of words in text, preserving single spaces.
    """
    words = text.strip().split()
    return " ".join(reversed(words))