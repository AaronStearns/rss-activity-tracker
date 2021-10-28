def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False