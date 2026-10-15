import requests
import time

from controller.controller import select_edge_server
from controller.controller import SERVERS
from controller.history_manager import add_observation
from controller.history_manager import get_history


selected_server, predictions = select_edge_server()

print("Predictions:")

for name, prediction in predictions.items():
    print(f"{name}: {prediction:.2f} ms")

selected_url = SERVERS[selected_server]

print()
print(f"Selected server: {selected_server}")
print(f"Sending request to {selected_url}")

start_time = time.perf_counter()

response = requests.get(
    f"{selected_url}/process",
    timeout=5
)

end_time = time.perf_counter()

response.raise_for_status()

actual_response_time = (end_time - start_time) * 1000

add_observation(
    selected_server,
    {
        "response_time": actual_response_time
    }
)

print()
print("Recent history:")
print(get_history(selected_server))

print()
print("Server response:")
print(response.json())

print()
print(f"Actual response time: {actual_response_time:.2f} ms")
print(
    f"Predicted response time: "
    f"{predictions[selected_server]:.2f} ms"
)
