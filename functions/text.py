def get_unicode_point(char: str) -> str:
    """
    Returns a Unicode point as an integer for a given character.
    Args:
        character (str): The character to lookup.
    Returns:
        int: The Unicode point as an integer.

    Examples:
        >>> get_unicode_point('A')
        'U+0041'
        >>> get_unicode_point('€')
        'U+20AC'
        >>> get_unicode_point('😃')
        'U+1F603'
    """
    if len(char) != 1:
        raise Exception('character must be a single character')
    return f'U+{ord(char):04X}'
