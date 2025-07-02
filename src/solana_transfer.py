from dotenv import load_dotenv
import os
import requests
import sqlite3
from datetime import datetime
from src.config import TOKENS

#  Load API key from .env inside /data
load_dotenv(dotenv_path=os.path.join("data", ".env"))
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

#  Wallet to track
WALLET = "J14Cg556roeBSgWFEKNTiSQeydMPRW6FZNB2zDMmSadQ"

#  Database path
DB_PATH = os.path.join("data", "transfers.db")

#  Ensure DB and table exist
def init_db():
    os.makedirs("data", exist_ok=True)  # Create 'data/' if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transfers (
            wallet TEXT,
            token TEXT,
            from_address TEXT,
            to_address TEXT,
            amount REAL,
            signature TEXT PRIMARY KEY,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

#  Initialize DB (auto-create if not exist)
init_db()

#  Fetch and store transfers
def fetch_transfers(wallet=WALLET):
    print(f"\n📡 Fetching transfers for wallet: {wallet}")
    url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions?api-key={HELIUS_API_KEY}&limit=10"

    try:
        res = requests.get(url)
        data = res.json()

        new_rows = 0

        # ✅ Use thread-safe DB connection
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        for tx in data:
            sig = tx.get("signature")
            ts = datetime.utcfromtimestamp(tx.get("timestamp")).isoformat()

            for t in tx.get("tokenTransfers", []):
                mint = t.get("mint")
                symbol = next((tok["symbol"] for tok in TOKENS if tok["mint"] == mint), "UNKNOWN")

                row = (
                    wallet,
                    symbol,
                    t.get("fromUserAccount"),
                    t.get("toUserAccount"),
                    t.get("tokenAmount"),
                    sig,
                    ts
                )
                try:
                    c.execute("INSERT INTO transfers VALUES (?, ?, ?, ?, ?, ?, ?)", row)
                    new_rows += 1
                except sqlite3.IntegrityError:
                    pass  # Duplicate entry, skip

        conn.commit()
        conn.close()

        print(f" Done. {new_rows} new transfer(s) inserted.")
        return new_rows

    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

#  Manual run
if __name__ == "__main__":
    fetch_transfers()
