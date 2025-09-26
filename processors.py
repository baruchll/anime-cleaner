import json
import subprocess
import os
from pathlib import Path
from utils import log_error, save_processed_file

def parse_env_list(var_name: str) -> set[str]:
    raw = os.getenv(var_name)
    if not raw:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return {lang.strip() for lang in raw.split(",")}

ALLOWED_SUBS = parse_env_list("ALLOWED_SUBS")
ALLOWED_AUDIO = parse_env_list("ALLOWED_AUDIO")

def get_track_info(file_path: Path):
    """Identify tracks and return JSON track list."""
    try:
        result = subprocess.run(
            ["mkvmerge", "--identify", "--identification-format", "json", str(file_path)],
            check=True, capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        return data.get("tracks", [])
    except Exception as e:
        log_error(file_path, f"Track identification failed: {e}")
        print(f"[ERROR] Track identification failed for {file_path}: {e}")
        return []

def needs_processing(tracks):
    """Return True if the file needs fixing, False if already correct."""
    english_audio_ok = False
    subs_ok = True
    for t in tracks:
        if t["type"] == "audio" and t["properties"].get("language") == "eng":
            if t["properties"].get("default_track") is True:
                english_audio_ok = True
        if t["type"] == "subtitles":
            lang = t["properties"].get("language")
            if lang not in ALLOWED_SUBS:
                subs_ok = False
    return not (english_audio_ok and subs_ok)

def process_file(file_path: Path):
    temp_file = file_path.with_suffix(".processed.mkv")
    try:
        tracks = get_track_info(file_path)
        if not tracks:
            print(f"[WARN] Skipping {file_path}, no track info")
            return ("failed", file_path)

        if not needs_processing(tracks):
            msg = f"⏩ Skipped (already fixed): {file_path.name}"
            print(f"[INFO] {msg}")
            return ("skipped", file_path)

        # Find first English audio track
        eng_audio_id = None
        for t in tracks:
            if t["type"] == "audio" and t["properties"].get("language") == "eng":
                eng_audio_id = t["id"]
                break
        if eng_audio_id is None:
            raise RuntimeError("No English audio track found")

        # Build mkvmerge command
        command = [
            "mkvmerge",
            "-o", str(temp_file),
            "--default-track", "0:yes",
            "--default-track", f"{eng_audio_id}:yes",
            "--audio-tracks", ",".join(ALLOWED_AUDIO),
            "--subtitle-tracks", ",".join(ALLOWED_SUBS),
            str(file_path),
        ]

        print(f"[INFO] Running: {' '.join(command)}")

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        if process.stdout is not None:
            for line in process.stdout:
                print(f"[MKVMERGE] {line}", end="")

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

        if not temp_file.exists() or temp_file.stat().st_size == 0:
            raise RuntimeError("Processed file missing or empty")

        temp_file.replace(file_path)
        save_processed_file(file_path)

        msg = f"✅ Processed: {file_path.name}"
        print(f"[INFO] {msg}")
        return ("processed", file_path)

    except Exception as e:
        log_error(file_path, f"Processing Error: {e}")
        print(f"[ERROR] Processing Error: {e}")
        return ("failed", file_path)
    finally:
        try:
            if temp_file.exists():
                temp_file.unlink()
        except Exception:
            pass
