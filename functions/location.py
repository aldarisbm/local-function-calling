from uszipcode import SearchEngine


def get_zipcode(city: str, state: str) -> str:
    """
    Returns a zipcode for a given city and state.
    Args:
        city (str): City.
        state (str): State in two-letter abbreviation.
    Returns:
        str: The zipcode as a string.

    Examples:
        >>> get_zipcode("New York", "NY")
        '10001'
        >>> get_zipcode("Los Angeles", "CA")
        '90001'
        >>> get_zipcode("Chicago", "IL")
        '60601'
    """
    engine = SearchEngine()
    res = engine.by_city_and_state(city, state)
    return res[0].zipcode
