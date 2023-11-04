from datetime import datetime


def get_weekday(day: int, month: int, year: int) -> str:
    """
    Returns the weekday for a given date.
    Args:
        day (int): The day.
        month (int): The month.
        year (int): The year.
    Returns:
        str: The weekday of the date provided.

    Examples:
        >>> get_weekday(1, 1, 2023)
        'Sunday'
        >>> get_weekday(20, 5, 2023)
        'Saturday'
        >>> get_weekday(15, 11, 2022)
        'Tuesday'
    """
    date_dict = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
    }
    return date_dict[datetime(day=day, month=month, year=year).weekday()]
