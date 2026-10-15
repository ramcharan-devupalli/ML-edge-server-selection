from fastapi import FastAPI
from fastapi.responses import Response
import os
import psutil

app = FastAPI()
active_requests = 0
server_name = os.getenv("SERVER_NAME", "Edge")


@app.get("/")
def home():
    return {
        "server": server_name,
        "status": "running"
    }


@app.get("/status")
def status():
    return {
        "server": server_name,
        "status": "available",
        "cpu_usage": psutil.cpu_percent(interval=None),
        "memory_usage": psutil.virtual_memory().percent,
        "active_requests": active_requests
    }

@app.get("/process")
def process():
    global active_requests

    active_requests += 1

    response = {
        "server": server_name,
        "message": "Request processed successfully"
    }

    active_requests -= 1

    return response
@app.get("/throughput")

def throughput():
    data = b"x" * (1024 * 1024)
    return Response(content=data, media_type="application/octet-stream")
