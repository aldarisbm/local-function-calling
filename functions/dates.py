from datetime import datetime


def get_weekday(day: int, month: int, year: int) -> str:
    """
    Returns the weekday for a given date.
    Args:
        day (int): The day. eg: 1, 20, 19
        month (int): The month. eg: 12, 10, 5
        year (int): The year. eg: 2021, 1993, 1987
    Returns:
        str: The weekday of the date provided. eg: Monday, Tuesday, Friday, Saturday
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
