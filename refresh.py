"""
refresh.py
24-hour data refresh scheduler.
Pulls new data from MongoDB, exports txt files, re-runs GraphRAG index.
Run this as a background process: python refresh.py
"""
import time
import subprocess
import os
import sys
from datetime import datetime

REFRESH_INTERVAL = 24 * 60 * 60  # 24 hours in seconds

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def refresh():
    log("Starting 24h data refresh...")

    # Step 1: Export from MongoDB to txt files
    try:
        from mongo_loader import export_to_txt
        export_to_txt()
        log("✅ Exported articles from MongoDB")
    except Exception as e:
        log(f"⚠️ MongoDB export failed: {e} — using existing txt files")

    # Step 2: Re-run GraphRAG indexing
    log("Starting GraphRAG re-indexing...")
    env = os.environ.copy()
    env["GRAPHRAG_API_KEY"] = "AQ.Ab8RN6IucCWAH3HiQV9oAxvnY4iQzYUKdSxLt4ZzJd4hEZPPRw"
    env["GRAPHRAG_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta/openai/"

    result = subprocess.run(
        [sys.executable, "-m", "graphrag.index", "--root", "."],
        env=env,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        log("✅ GraphRAG re-indexing complete")
    else:
        log(f"⚠️ GraphRAG indexing error: {result.stderr[-500:]}")

    log(f"Next refresh in 24 hours")

if __name__ == "__main__":
    log("🔄 Refresh scheduler started")
    while True:
        refresh()
        time.sleep(REFRESH_INTERVAL)
