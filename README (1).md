#  Solana SPL Token Tracker

This is a full-stack application that tracks and visualizes SPL token transfer activity for a specific Solana wallet. It uses:

-  **FastAPI** for building RESTful APIs
-  **SQLite** for storing transfer data
-  **Streamlit** for interactive dashboard and data filtering
-  **Helius API** to fetch Solana blockchain transaction data

---

##  Overview

This project tracks SPL token transfers for a given Solana wallet using the [Helius API](https://www.helius.xyz/), stores the data in a local SQLite database, exposes the data via FastAPI, and visualizes it in an interactive Streamlit dashboard.

---

##  Getting Started

###  Prerequisites

- Python 3.10 or later
- Pip or virtualenv
- `.env` file inside `data/` folder with your Helius API key:

```
HELIUS_API_KEY=your_helius_api_key_here
```

---

###  Installation

```bash

# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
```

---

###  Run the Application

```bash
python main.py
```

This will launch both the FastAPI server and Streamlit dashboard.

---

##  API Endpoints

### Root
**`GET /`**  
Returns a welcome message and documentation link.

---

### Token Info
**`GET /token-info`**  
Returns metadata about supported tokens (mint address, symbol).

---

### Transfer History
**`GET /transfers/{wallet_address}`**  
Returns a list of token transfer records for the specified wallet.

Example:  
`GET /transfers/J14Cg556roeBSgWFEKNTiSQeydMPRW6FZNB2zDMmSadQ`

---

### Transfer Chart Data
**`GET /chart-data`**  
Returns aggregated transfer volume per token over time (used for plotting charts in the dashboard).

---

### Update Data
**`POST /update-data`**  
Triggers a background fetch using Helius API to get the latest transactions and store new ones in the database.

Returns a message with the number of new transfers inserted.

---

##  Project Structure

```
.
intern_assessment/
├── data/
│   ├── .env                 # Environment variables (API key)
│   └── transfers.db         # SQLite database (auto-created)
├── src/
│   ├── config.py            # Token mint configurations
│   ├── solana_transfer.py   # Fetch & store transfer logic
│   ├── solana_api.py        # FastAPI application
│   └── solana_tracker.py    # Streamlit dashboard code
├── main.py                  # Launches API and dashboard
├── requirements.txt         # Python dependencies
├── .env.example             # Example env file
└── .gitignore               # Specifies untracked files
```

---

##  Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Helius API](https://www.helius.xyz/)
- [SQLite](https://www.sqlite.org/)
- [Plotly](https://plotly.com/python/)

---



