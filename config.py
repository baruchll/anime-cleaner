import os


def parse_env_list(var_name: str) -> set[str]:
    """Parse a comma-separated env var into a set of values."""
    raw = os.getenv(var_name)
    if not raw:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return {lang.strip() for lang in raw.split(",")}


# --- Mode ---
MODE = os.getenv("MODE", "anime")

if MODE == "anime":
    LIBRARY_PATHS = [
        ("Anime Series", os.getenv("ANIME_SERIES_PATH")),
        ("Anime Movies", os.getenv("ANIME_MOVIES_PATH")),
    ]
    ALLOWED_AUDIO = parse_env_list("ANIME_ALLOWED_AUDIO")
    ALLOWED_SUBS = parse_env_list("ANIME_ALLOWED_SUBS")

elif MODE == "movies":
    LIBRARY_PATHS = [
        ("Movies", os.getenv("MOVIES_PATH")),
        ("TV", os.getenv("TV_PATH")),
    ]
    ALLOWED_AUDIO = parse_env_list("MOVIES_ALLOWED_AUDIO")
    ALLOWED_SUBS = parse_env_list("MOVIES_ALLOWED_SUBS")

else:
    raise RuntimeError(f"Invalid MODE: {MODE}")


# --- Common settings ---
MAX_WORKERS = int(os.getenv("MAX_WORKERS", 4))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
