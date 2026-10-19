from controller.network_monitor import collect_features
from controller.predictor import predict_response_time
from controller.selector import select_server


SERVERS = {
    "Edge-A": "http://127.0.0.1:8001",
    "Edge-B": "http://127.0.0.1:8002",
    "Edge-C": "http://127.0.0.1:8003"
}


def select_edge_server():

    predictions = {}

    for name, url in SERVERS.items():

        features = collect_features(name, url)

        prediction = predict_response_time(features)

        predictions[name] = prediction

    selected_server = select_server(predictions)

    return selected_server, predictions
