import joblib
import pandas as pd

MODEL_FILE = "model/trained_model.pkl"

FEATURES = [
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

model = joblib.load(MODEL_FILE)


def predict_response_time(feature_values):
    data = pd.DataFrame(
        [feature_values],
        columns=FEATURES
    )

    prediction = model.predict(data)

    return prediction[0]
