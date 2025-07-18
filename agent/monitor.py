# agent/monitor.py

import time
import platform
import psutil
import requests
import logging
from datetime import datetime

# Set the backend API endpoint (adjust this to your backend service URL)
BACKEND_API_URL = "http://localhost:8000/api/metrics"

# Optional: machine identifier (hostname, UUID, etc.)
AGENT_ID = platform.node()

# Configure logging
logging.basicConfig(
    filename='agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def collect_metrics():
    """
    Collect system metrics like CPU, memory, disk usage, etc.
    """
    return {
        "agent_id": AGENT_ID,
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "load_avg": psutil.getloadavg() if hasattr(psutil, "getloadavg") else None,
        "boot_time": datetime.utcfromtimestamp(psutil.boot_time()).isoformat()
    }

def send_to_backend(metrics):
    """
    Send the collected metrics to the backend API.
    """
    try:
        response = requests.post(BACKEND_API_URL, json=metrics)
        response.raise_for_status()
        logging.info("Metrics sent successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to send metrics: {e}")

def run_agent(interval=10):
    """
    Start the monitoring loop.
    """
    logging.info("Agent started.")
    while True:
        metrics = collect_metrics()
        logging.info(f"Collected metrics: {metrics}")
        send_to_backend(metrics)
        time.sleep(interval)

if __name__ == "__main__":
    run_agent(interval=10)
