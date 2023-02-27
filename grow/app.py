from chalice import Chalice
from enum import Enum


from chalicelib.wikipedia.period import weekly_view_sum, top, sum_between

app = Chalice(app_name="grow")


class GRANULARITY(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@app.route("/top", methods=["POST"])
def route_top():
    json_body = app.current_request.json_body
    result = {}

    if json_body.get("granularity") == GRANULARITY.DAILY.value:
        result = top(
            json_body.get("project"),
            json_body.get("year"),
            json_body.get("month"),
            json_body.get("day"),
            json_body.get("access"),
        )
    elif json_body.get("granularity") == GRANULARITY.WEEKLY.value:
        result = weekly_view_sum(
            json_body.get("project"),
            json_body.get("year"),
            json_body.get("month"),
            json_body.get("day"),
            json_body.get("access"),
        )
    elif json_body.get("granularity") == GRANULARITY.MONTHLY.value:
        result = top(
            json_body.get("project"),
            json_body.get("year"),
            json_body.get("month"),
            "all-days",
            json_body.get("access"),
        )

    return result


@app.route("/top/{article}", methods=["POST"])
def route_top_by_article(article):
    json_body = app.current_request.json_body
    result = sum_between(
        json_body.get("project"),
        article,
        json_body.get("start_date"),
        json_body.get("end_date"),
        agent="all-agents",
        access="all-access",
    )

    return result
