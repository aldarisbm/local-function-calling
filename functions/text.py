def get_unicode_point(char: str) -> str:
    """
    Returns a Unicode point as an integer for a given character.
    Args:
        char (str): The character to lookup.
    Returns:
        int: The Unicode point as an integer.
    Raises:
        ValueError: If the string is longer than 1 character

    Examples:
        >>> get_unicode_point('A')
        'U+0041'
        >>> get_unicode_point('€')
        'U+20AC'
        >>> get_unicode_point('😃')
        'U+1F603'
    """
    if len(char) != 1:
        raise ValueError('character must be a single character')
    return f'U+{ord(char):04X}'
