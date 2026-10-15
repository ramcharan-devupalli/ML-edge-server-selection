import time
import requests
import subprocess
from controller.data_collector import save_observation
from controller.feature_builder import build_features

from controller.history_manager import (
    add_observation,
    get_recent_average_response_time,
    get_response_time_trend,
    get_recent_failure_count
)

def measure_latency(server_url):
    start_time = time.perf_counter()

    response = requests.get(
        f"{server_url}/status",
        timeout=2
    )

    end_time = time.perf_counter()

    response.raise_for_status()

    latency_ms = (end_time - start_time) * 1000

    return latency_ms

def measure_packet_loss(host):
    result = subprocess.run(
        ["ping", "-c", "4", "-W", "1", host],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "packet loss" in line:
            loss_part = line.split(",")[2]
            return float(loss_part.strip().split("%")[0])

    return 100.0

def measure_throughput(server_url):
    start_time = time.perf_counter()

    response = requests.get(
        f"{server_url}/throughput",
        timeout=5
    )

    end_time = time.perf_counter()

    response.raise_for_status()

    elapsed_time = end_time - start_time
    bytes_received = len(response.content)

    throughput_mbps = (bytes_received * 8) / elapsed_time / 1_000_000

    return throughput_mbps

def measure_response_time(server_url):
    start_time = time.perf_counter()

    response = requests.get(
        f"{server_url}/process",
        timeout=5
    )

    end_time = time.perf_counter()

    response.raise_for_status()

    response_time_ms = (end_time - start_time) * 1000

    return response_time_ms

def collect_features(server, server_url):
    status_response = requests.get(
        f"{server_url}/status",
        timeout=2
    )

    status_response.raise_for_status()

    status = status_response.json()

    latency = measure_latency(server_url)
    packet_loss = measure_packet_loss("127.0.0.1")
    throughput = measure_throughput(server_url)

    current_features = [
    latency,
    packet_loss,
    throughput,
    status["cpu_usage"],
    status["memory_usage"],
    status["active_requests"]
    ]

    return build_features(server, current_features)

if __name__ == "__main__":
    servers = {
        "Edge-A": "http://127.0.0.1:8001",
        "Edge-B": "http://127.0.0.1:8002",
        "Edge-C": "http://127.0.0.1:8003"
    }

    while True:
        for name, url in servers.items():

            status_response = requests.get(
                f"{url}/status",
                timeout=2
            )

            status_response.raise_for_status()

            status = status_response.json()

            latency = measure_latency(url)
            packet_loss = measure_packet_loss("127.0.0.1")
            throughput = measure_throughput(url)
            response_time = measure_response_time(url)

            recent_average = get_recent_average_response_time(name)

            if recent_average is None:
                recent_average = 0.0
            response_time_trend = get_response_time_trend(name)
            recent_failure_count = get_recent_failure_count(name)

            observation = {
                "server": name,
                "latency": latency,
                "packet_loss": packet_loss,
                "throughput": throughput,
                "cpu_usage": status["cpu_usage"],
                "memory_usage": status["memory_usage"],
                "active_requests": status["active_requests"],
                "recent_avg_response_time": recent_average,
                "response_time_trend": response_time_trend,
                "recent_failure_count": recent_failure_count,
                "response_time": response_time
            }

            save_observation(observation)

            add_observation(
                name,
                {
                    "response_time": response_time
                }
            )

            print(
                f"{name}: "
                f"latency={latency:.2f} ms, "
                f"packet_loss={packet_loss:.2f}%, "
                f"throughput={throughput:.2f} Mbps, "
                f"cpu={status['cpu_usage']:.2f}%, "
                f"memory={status['memory_usage']:.2f}%, "
                f"active_requests={status['active_requests']}, "
                f"response_time={response_time:.2f} ms"
            )

        print("Waiting for next collection...\n")
        time.sleep(5)

