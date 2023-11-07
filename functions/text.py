def get_unicode_point(char: str) -> str:
    """
    Returns a Unicode point as str for a given character, char must be of len=1.
    Args:
        char (str): The character to lookup.
    Returns:
        int: The Unicode point as a unicode string.
    Raises:
        ValueError: If the string is longer than 1 character
    Examples:
        >>> get_unicode_point(char='A')
        'U+0041'
        >>> get_unicode_point(char='€s')
        ValueError
        >>> get_unicode_point(char='😃')
        'U+1F603'
    """
    if len(char) != 1:
        raise ValueError('character must be a single character')
    return f'U+{ord(char):04X}'
