from collections import defaultdict, deque


MAX_HISTORY = 5

history = defaultdict(lambda: deque(maxlen=MAX_HISTORY))


def add_observation(server, observation):
    history[server].append(observation)


def get_history(server):
    return list(history[server])


def get_recent_average_response_time(server):
    observations = get_history(server)

    if not observations:
        return None

    total = sum(
        observation["response_time"]
        for observation in observations
    )

    return total / len(observations)


def get_response_time_trend(server):
    observations = get_history(server)

    if len(observations) < 4:
        return 0.0

    middle = len(observations) // 2

    older = observations[:middle]
    recent = observations[middle:]

    older_average = sum(
        observation["response_time"]
        for observation in older
    ) / len(older)

    recent_average = sum(
        observation["response_time"]
        for observation in recent
    ) / len(recent)

    return recent_average - older_average


def get_recent_failure_count(server):
    observations = get_history(server)

    return sum(
        1
        for observation in observations
        if observation.get("failed", False)
    )