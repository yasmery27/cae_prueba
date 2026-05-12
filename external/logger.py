from datetime import datetime


def log_error(error_message):
    timestamp = datetime.utcnow().isoformat()
    return f"[ERROR] {timestamp} - {error_message}"
