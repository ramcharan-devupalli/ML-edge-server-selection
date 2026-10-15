import pandas as pd


DATA_FILE = "data/processed/dataset.csv"

features = [
    "latency",
    "packet_loss",
    "throughput",
    "cpu_usage",
    "memory_usage",
    "active_requests"
]

target = "response_time"


df = pd.read_csv(DATA_FILE)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print()
print("Missing values:")
print(df.isnull().sum())

print()
print("Duplicate rows:", df.duplicated().sum())

print()
print("Invalid numerical values:")
print(df[features + [target]].isin([float("inf"), float("-inf")]).sum())

print()
print("Required columns present:")
print(set(features + [target]).issubset(df.columns))
