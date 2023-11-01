from datetime import datetime


def get_weekday(day: int, month: int, year: int) -> str:
    """
    Returns the weekday for the provided date

    Args:
        day (int): The day
        month (int): The month
        year (int): The year

    Returns:
        str: The weekday of the date provided
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


print(get_weekday.__doc__)
