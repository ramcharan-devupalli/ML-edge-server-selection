import requests

def send_request(server_url):
    response = requests.get(f"{server_url}/process")
    return response.json()

server_url = "http://127.0.0.1:8001"

result = send_request(server_url)

print(result)
