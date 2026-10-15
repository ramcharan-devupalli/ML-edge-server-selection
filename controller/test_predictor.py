import requests

from predictor import predict_response_time


servers = {
    "Edge-A": "http://127.0.0.1:8001",
    "Edge-B": "http://127.0.0.1:8002",
    "Edge-C": "http://127.0.0.1:8003"
}

for name, url in servers.items():

    response = requests.get(
        f"{url}/status",
        timeout=2
    )

    response.raise_for_status()

    status = response.json()

    features = [
        status["latency"] if "latency" in status else 0,
        0,
        0,
        status["cpu_usage"],
        status["memory_usage"],
        status["active_requests"]
    ]

    prediction = predict_response_time(features)

    print(
        f"{name}: "
        f"Predicted response time = {prediction:.2f} ms"
    )
