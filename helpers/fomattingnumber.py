from datetime import timedelta


def time_format(seconds: int, format_string="%h%m%s"):
    primary = str(timedelta(seconds=seconds))
    parts = primary.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    second = int(parts[2])

    if hours != 0:
        format_string = format_string.replace("%h", str(hours) + "hours ")
    else:
        format_string = format_string.replace("%h", "")
    if minutes != 0:
        format_string = format_string.replace("%m", str(minutes) + "minutes ")
    else:
        format_string = format_string.replace("%m", "")
    return format_string.replace("%s", str(second) + "seconds ")


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
