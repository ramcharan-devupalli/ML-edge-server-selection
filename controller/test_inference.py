from controller.network_monitor import collect_features
from controller.predictor import predict_response_time


server_url = "http://127.0.0.1:8001"

features = collect_features("Edge-A", server_url)

prediction = predict_response_time(features)

print("Features:")
print(features)

print()
print(f"Predicted response time: {prediction:.2f} ms")
