def flatten(lst: list) -> list:
    """
    Flatten a nested list of arbitrary depth.
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result