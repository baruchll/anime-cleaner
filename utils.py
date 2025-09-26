import os
import json
import requests
from pathlib import Path

def require_env(var_name: str) -> str:
    """Require an environment variable or raise an error."""
    value = os.getenv(var_name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value

# Required env vars
BOT_TOKEN = require_env("TELEGRAM_BOT_TOKEN")
CHAT_ID = require_env("TELEGRAM_CHAT_ID")

# Optional env vars (logs only if provided)
ERROR_LOG = os.getenv("ERROR_LOG")
PROCESSED_FILES_LOG = os.getenv("PROCESSED_FILES_LOG")


def log_error(file_path, error_message):
    """Write error log entry and always print to console."""
    if ERROR_LOG:
        error_data = {"file": str(file_path), "error": error_message}
        with open(Path(ERROR_LOG), "a") as log_file:
            log_file.write(json.dumps(error_data) + "\n")
    print(f"[ERROR] {file_path}: {error_message}")


def save_processed_file(file_path):
    """Write processed file log entry and always print to console."""
    if PROCESSED_FILES_LOG:
        with open(Path(PROCESSED_FILES_LOG), "a") as log_file:
            log_file.write(str(file_path) + "\n")
    print(f"[INFO] Saved processed file: {file_path}")


def send_telegram_notification(message):
    """Send message to Telegram, fail loudly if bot token/chat ID missing."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[ERROR] Telegram Notification Failed: {e}")
