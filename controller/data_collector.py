import csv
import os


DATA_FILE = "data/raw/observations.csv"


def save_observation(observation):
    file_exists = os.path.exists(DATA_FILE)

    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "server",
                "latency",
                "packet_loss",
                "throughput",
                "cpu_usage",
                "memory_usage",
                "active_requests",
                "recent_avg_response_time",
                "response_time_trend",
                "recent_failure_count",
                "response_time"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(observation)
