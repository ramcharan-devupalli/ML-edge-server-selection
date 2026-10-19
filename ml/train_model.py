import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


DATA_FILE = "data/processed/dataset.csv"


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


df = pd.read_csv(DATA_FILE)

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(model, "model/trained_model.pkl")
print("Model saved to model/trained_model.pkl")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("MAE:", mae)
print("RMSE:", rmse)

print()
print("Actual vs Predicted:")

for actual, predicted in zip(y_test, predictions):
    print(
        f"Actual: {actual:.2f} ms, "
        f"Predicted: {predicted:.2f} ms"
    )

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))
print("Model training completed")
