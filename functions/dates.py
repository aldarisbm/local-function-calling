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
        >>> get_weekday(day=1, month=1, year=2023)
        'Sunday'
        >>> get_weekday(day=20, month=5, year=2023)
        'Saturday'
        >>> get_weekday(day=15, month=11, year=2022)
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


def get_date() -> str:
    """
    Returns today's date as a string
    Returns:
        str: Today's date.

    Examples:
        >>> get_date()
        '2023-01-06 11:15:37.063665'
        >>> get_date()
        '2023-11-16 12:31:37.063665'
        >>> get_date()
        '2023-04-01 05:20:37.063665'
    """
    return str(datetime.today())
