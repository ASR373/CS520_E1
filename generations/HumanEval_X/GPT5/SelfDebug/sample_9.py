def remove_duplicates(seq: list) -> list:
    """
    Remove duplicates from seq while preserving original order.
    """
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result