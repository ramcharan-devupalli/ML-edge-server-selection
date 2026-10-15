from controller.history_manager import (
    get_recent_average_response_time,
    get_response_time_trend,
    get_recent_failure_count
)


def build_features(server, current_features):
    recent_average = get_recent_average_response_time(server)

    if recent_average is None:
        recent_average = 0.0

    response_time_trend = get_response_time_trend(server)

    recent_failure_count = get_recent_failure_count(server)

    return current_features + [
        recent_average,
        response_time_trend,
        recent_failure_count
    ]
