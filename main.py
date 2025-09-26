import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from processors import process_file
from utils import send_telegram_notification

def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value

# Two separate libraries
SERIES_PATH = require_env("ANIME_SERIES_PATH")
MOVIES_PATH = require_env("ANIME_MOVIES_PATH")
MAX_WORKERS = int(require_env("MAX_WORKERS"))

def scan_directory(source_dir: str):
    video_files = []
    for root, _, files in os.walk(source_dir):
        for f in files:
            if f.lower().endswith(('.mkv', '.mp4', '.avi', '.mov')):
                video_files.append(Path(root) / f)
    return video_files

def process_library(label: str, path: str, max_workers: int):
    files = scan_directory(path)
    total = len(files)
    processed = skipped = failed = 0

    print(f"[INFO] Starting batch for {label} ({total} files) at {path}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(process_file, p): p for p in files}
        for fut in as_completed(futures):
            try:
                status, _ = fut.result()
                if status == "processed": processed += 1
                elif status == "skipped": skipped += 1
                else: failed += 1
            except Exception:
                failed += 1

    return {
        "label": label,
        "total": total,
        "processed": processed,
        "skipped": skipped,
        "failed": failed,
    }

def standalone_mode():
    results = []
    results.append(process_library("Anime Series", SERIES_PATH, MAX_WORKERS))
    results.append(process_library("Anime Movies", MOVIES_PATH, MAX_WORKERS))

    # Build summary
    summary_lines = ["Ani Cleaner summary"]
    for r in results:
        summary_lines.append(
            f"{r['label']}: {r['total']} total | "
            f"{r['processed']} processed | "
            f"{r['skipped']} skipped | "
            f"{r['failed']} failed"
        )

    summary = "\n".join(summary_lines)
    print(f"[INFO] {summary}")
    send_telegram_notification(summary)

if __name__ == "__main__":
    standalone_mode()
