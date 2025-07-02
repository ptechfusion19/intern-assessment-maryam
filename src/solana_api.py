from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
import sqlite3
import pandas as pd
import os

from src.config import TOKENS
from src.solana_transfer import fetch_transfers

# Initialize FastAPI app
app = FastAPI(title="Solana Token Tracker API")

# Constants
DB = os.path.join("data", "transfers.db")
WALLET = "J14Cg556roeBSgWFEKNTiSQeydMPRW6FZNB2zDMmSadQ"

#  Utility: Get database connection
def get_conn():
    return sqlite3.connect(DB)

#  Root endpoint
@app.get("/")
def root():
    return JSONResponse({
        "message": "Solana Tracker API is running. Visit /docs for interactive API."
    })

#  GET /token-info
@app.get("/token-info")
def get_token_info():
    return TOKENS

#  GET /transfers/<wallet>
@app.get("/transfers/{wallet_address}")
def get_transfers(wallet_address: str):
    conn = get_conn()
    df = pd.read_sql(
        "SELECT * FROM transfers WHERE wallet = ? ORDER BY timestamp DESC",
        conn,
        params=(wallet_address,)
    )
    conn.close()

    if df.empty:
        raise HTTPException(status_code=404, detail="No transfers found for this wallet")

    return df.to_dict(orient="records")

#  GET /chart-data
@app.get("/chart-data")
def get_chart_data():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT token, timestamp, SUM(amount) as total_volume
        FROM transfers
        GROUP BY token, timestamp
        ORDER BY timestamp DESC
    """)
    rows = c.fetchall()
    conn.close()

    return [
        {"token": r[0], "timestamp": r[1], "total_volume": r[2]} for r in rows
    ]

#  POST /update-data
@app.post("/update-data")
def update_data():
    count = fetch_transfers(WALLET)
    return {
        "message": f"✅ Update complete. {count if count else 'None'} new token transfers inserted.",
        "updated_at": datetime.utcnow().isoformat()
    }
