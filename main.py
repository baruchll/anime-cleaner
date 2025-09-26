import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from processors import process_file
from utils import send_telegram_notification

# Helper to enforce required variables
def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value

# Required settings (must exist in .env)
LIBRARY_PATH = require_env("ANIME_LIBRARY_PATH")
MAX_WORKERS = int(require_env("MAX_WORKERS"))

def scan_directory(source_dir: str):
    video_files = []
    for root, _, files in os.walk(source_dir):
        for f in files:
            if f.lower().endswith(('.mkv', '.mp4', '.avi', '.mov')):
                video_files.append(Path(root) / f)
    return video_files

def standalone_mode():
    files = scan_directory(LIBRARY_PATH)
    total = len(files)
    processed = skipped = failed = 0

    print(f"[INFO] Starting batch on {LIBRARY_PATH} ({total} files)")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(process_file, p): p for p in files}
        for fut in as_completed(futures):
            try:
                status, _ = fut.result()
                if status == "processed": processed += 1
                elif status == "skipped": skipped += 1
                else: failed += 1
            except Exception:
                failed += 1

    summary = f"Anime fixer summary\nTotal: {total}\nProcessed: {processed}\nSkipped: {skipped}\nFailed: {failed}"
    print(f"[INFO] {summary}")
    send_telegram_notification(summary)

if __name__ == "__main__":
    standalone_mode()
