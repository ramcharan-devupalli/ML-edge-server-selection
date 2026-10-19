import pandas as pd


RAW_FILE = "data/raw/observations.csv"
PROCESSED_FILE = "data/processed/dataset.csv"


df = pd.read_csv(RAW_FILE)

features = [
    "latency",
    "packet_loss",
    "throughput",
    "cpu_usage",
    "memory_usage",
    "active_requests",
    "recent_avg_response_time",
    "response_time_trend",
    "recent_failure_count"
]

target = "response_time"

dataset = df[features + [target]]

dataset.to_csv(PROCESSED_FILE, index=False)

print(dataset)
print()
print(f"Saved dataset to {PROCESSED_FILE}")
