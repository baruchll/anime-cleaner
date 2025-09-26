import time
import schedule
import subprocess
import os

def run_fixer():
    print("[INFO] Starting daily anime fixer run...")
    try:
        subprocess.run(
            ["python", "/anime_fixer/main.py"],
            check=True,
            env={**os.environ, "FIXER_MODE": "standalone"},
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Anime fixer failed: {e}")

def main():
    # Run once at startup
    run_fixer()
    # Schedule once per day at midnight
    schedule.every().day.at("00:00").do(run_fixer)

    print("[INFO] Anime fixer scheduler started. Next run at 00:00")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
