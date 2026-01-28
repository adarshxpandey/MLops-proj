from datetime import datetime

LOG_FILE = "app.log"

def log_event(message: str):
    with open(LOG_FILE, "a") as file:
        file.write(f"[{datetime.now().isoformat()}] {message}\n")
