import sys
import os
import subprocess
import time

# Ensure 'src' is in the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from solana_transfer import init_db  # now works because init_db exists in src/solana_transfer.py

# Use dot notation for FastAPI app and file path for Streamlit
api_path = "src.solana_api:app"
dashboard_path = "src/solana_tracker.py"

# ✅ Ensure database folder + table are ready
init_db()

# Start FastAPI server
api_process = subprocess.Popen(["uvicorn", api_path, "--reload"])

# Wait for API to be fully initialized before launching dashboard
time.sleep(2)

# Start Streamlit dashboard
dashboard_process = subprocess.Popen(["streamlit", "run", dashboard_path])

try:
    print("✅ Both API and Dashboard are running.")
    print("📡 FastAPI → http://127.0.0.1:8000/docs")
    print("📊 Dashboard → http://localhost:8501")

    # Wait for both processes to complete
    api_process.wait()
    dashboard_process.wait()

except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    api_process.terminate()
    dashboard_process.terminate()
