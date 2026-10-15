from controller.network_monitor import collect_features
from controller.predictor import predict_response_time
from controller.selector import select_server


servers = {
    "Edge-A": "http://127.0.0.1:8001",
    "Edge-B": "http://127.0.0.1:8002",
    "Edge-C": "http://127.0.0.1:8003"
}

predictions = {}

for name, url in servers.items():

    features = collect_features(url)

    prediction = predict_response_time(features)

    predictions[name] = prediction

    print(
        f"{name}: "
        f"Predicted response time = {prediction:.2f} ms"
    )

selected_server = select_server(predictions)

print()
print(f"Selected server: {selected_server}")
