import datetime


def __week_list_from_day__(datetime_str):
    """
    Gets a list of dates [(YYYY, MM, DD), ...)
    for a week given a single day"""
    datetime_object = datetime.datetime.strptime(datetime_str, "%Y/%m/%d")
    weekday = datetime_object.isoweekday()
    start = datetime_object - datetime.timedelta(days=weekday)
    dates = [start + datetime.timedelta(days=d) for d in range(7)]
    return [(d.year, d.month, d.day) for d in dates]


def __today__():
    """Date of the day as YYYYmmdd format."""
    return datetime.date.today().strftime("%Y%m%d")


def __days_ago__(days):
    """Days ago as YYYYmmdd format."""
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    ago = today - delta
    return ago.strftime("%Y%m%d")


def __avg__(numeric_list):
    """Basic average function."""
    return sum(numeric_list) / float(len(numeric_list))


def __sum_nested__(nested_response):
    """Basic average function."""
    summed_views = {}
    for item in nested_response:
        for j in item.get("items")[0].get("articles"):
            key = j.get("article")

            if key in summed_views:
                summed_views[key] += j.get("views")
            else:
                summed_views[key] = j.get("views")
    return summed_views
