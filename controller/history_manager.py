
import json
import os
from filelock import FileLock
from collections import defaultdict, deque

MAX_HISTORY = 5
HISTORY_FILE = "data/raw/server_history.json"
LOCK_FILE = HISTORY_FILE + ".lock"
history_lock = FileLock(LOCK_FILE)

history = defaultdict(lambda: deque(maxlen=MAX_HISTORY))


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return

    try:
        with open(HISTORY_FILE, "r") as file:
            saved_history = json.load(file)

        for server, observations in saved_history.items():
            history[server] = deque(
                observations,
                maxlen=MAX_HISTORY
            )

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not load saved server history.")


def save_history():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    with open(HISTORY_FILE, "w") as file:
        json.dump(
            {server: list(observations)
             for server, observations in history.items()},
            file,
            indent=2
        )


def add_observation(server, observation):
    with history_lock:
        history.clear()
        load_history()

        if server not in history:
            history[server] = deque(maxlen=MAX_HISTORY)

        history[server].append(observation)
        save_history()


def get_history(server):
    with history_lock:
        history.clear()
        load_history()

        if server not in history:
            return []

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


load_history()

