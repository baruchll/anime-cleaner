import time
import schedule
import subprocess
import os


MODE = os.getenv("MODE", "anime")  # anime or movies


def run_fixer():
    print(f"[INFO] Starting daily {MODE} cleaner run...")
    try:
        subprocess.run(
            ["python", "/anime_fixer/main.py"],  # path inside container
            check=True,
            env={**os.environ, "FIXER_MODE": "standalone"},
        )
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {MODE.capitalize()} cleaner failed: {e}")


def main():
    # Run once at startup
    run_fixer()

    # Schedule once per day at midnight
    schedule.every().friday.at("23:00").do(run_fixer)

    print(f"[INFO] {MODE.capitalize()} cleaner scheduler started. Next run at 00:00")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
