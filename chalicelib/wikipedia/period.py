"""Helper functions on period."""
from chalicelib.wikipedia.client import per_article, top

from chalicelib.utils.utils import (
    __days_ago__,
    __today__,
    __avg__,
    __week_list_from_day__,
    __sum_nested__,
)


def sum_between(
    project, page, start_date, end_date, agent="all-agents", access="all-access"
):
    """Page views given start and end dates."""
    views = per_article(project, page, start_date, end_date, access=access, agent=agent)

    view_sum = sum([daily["views"] for daily in views["items"]])
    max_view = max(views.get("items"), key=lambda x: x["views"])

    print(max_view)

    views["total_views"] = view_sum
    views["max_view"] = max_view

    return views


def sum_last(project, page, last=30, agent="all-agents", access="all-access"):
    """Page views during last days."""
    views = per_article(
        project, page, __days_ago__(last), __today__(), access=access, agent=agent
    )
    return sum([daily["views"] for daily in views["items"]])


def avg_last(project, page, last=30, agent="all-agents", access="all-access"):
    """Page views during last days."""
    views = per_article(
        project, page, __days_ago__(last), __today__(), access=access, agent=agent
    )
    return __avg__([daily["views"] for daily in views["items"]])


def weekly_view_sum(project, year, month, day, access="all-access"):
    datetime_str = year + "/" + month + "/" + day

    response_dates = __week_list_from_day__(datetime_str)

    response_object = []
    for date_tuple in response_dates:
        response = top(
            project,
            date_tuple[0],
            str(date_tuple[1]).zfill(2),
            str(date_tuple[2]).zfill(2),
            access=access,
        )
        response_object.append(response)
    summed_views = __sum_nested__(response_object)
    sorted_by_views = sorted(summed_views.items(), key=lambda x: x[1], reverse=True)
    response = [
        {"article": j[0], "views": j[1], "rank": i + 1}
        for i, j in enumerate(sorted_by_views)
    ]

    result = {
        "items": [
            {
                "project": project,
                "access": access,
                "year": year,
                "month": str(month).zfill(2),
                "day": str(day).zfill(2),
                "articles": response,
            }
        ]
    }

    return result
