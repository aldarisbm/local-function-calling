def get_weather_forecast(zipcode: str) -> str:
    """
    Returns the weather forecast for a given zipcode.
    Args:
        zipcode (str): The zipcode to lookup.
    Returns:
        str: The weather forecast.

    Examples:
        >>> get_weather_forecast(zipcode="90210")
        'Partly cloudy with a chance of rain'
        >>> get_weather_forecast(zipcode="10001")
        'Sunny and clear skies'
        >>> get_weather_forecast(zipcode="60601")
        'Overcast with a chance of thunderstorms'
    """
    return "sunny"
