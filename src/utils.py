import isodate

def youtube_time_to_seconds(time):
    '''Converts youtube time to seconds\n
    Args: time (str): time in youtube format\n
    Returns: int: time in seconds\n
    
    Example:
    >>> youtube_time_to_seconds('PT1H2M3S')
    3723
    '''
    duration = isodate.parse_duration(time)
    return duration.total_seconds()

def seconds_to_days_with_x_times(seconds, x = 1):
    '''Converts seconds to days\n
    Args: seconds (int): time in seconds\n
    Args: x (int): speed of video\n
    Returns: str: time in days\n
    
    Example:
    >>> seconds_to_days(3723, 1.25)
    '1 day, 2 hours, 59 minutes, 54 seconds'

    >>> seconds_to_days(3723, 1.50)
    '1 day, 1 hours, 59 minutes, 54 seconds'

    >>> seconds_to_days(3723, 2.00)
    '1 day, 1 hours, 29 minutes, 54 seconds'
    '''
    seconds = seconds / x
    days = seconds // (24 * 3600)
    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    seconds = int(seconds)
    if days == 0:
        return f'{hours} hours, {minutes} minutes, {seconds} seconds'
    else:
        return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'
