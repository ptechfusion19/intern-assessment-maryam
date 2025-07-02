import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from solana_transfer import init_db  # ✅ Ensure DB/table created

# Initialize database
init_db()

# Constants
API_BASE = "http://localhost:8000"
WALLET = "J14Cg556roeBSgWFEKNTiSQeydMPRW6FZNB2zDMmSadQ"

# Streamlit page setup
st.set_page_config(layout="wide")
st.title("📊 Solana SPL Token Tracker (API-Based)")

#  Fetch transfer data from API
@st.cache_data(ttl=60)
def fetch_transfer_data(wallet):
    try:
        res = requests.get(f"{API_BASE}/transfers/{wallet}")
        if res.status_code == 200:
            return pd.DataFrame(res.json())
    except Exception as e:
        st.error(f"Failed to fetch transfer data: {e}")
    return pd.DataFrame()

#  Fetch chart data from API
@st.cache_data(ttl=60)
def fetch_chart_data():
    try:
        res = requests.get(f"{API_BASE}/chart-data")
        if res.status_code == 200:
            return pd.DataFrame(res.json())
    except Exception as e:
        st.error(f"Failed to fetch chart data: {e}")
    return pd.DataFrame()

#  Manual refresh button
if st.button("🔄 Refresh Data"):
    try:
        requests.post(f"{API_BASE}/update-data")
        st.cache_data.clear()
    except:
        st.error("Failed to trigger update.")

# Load data from API
df = fetch_transfer_data(WALLET)
chart_df = fetch_chart_data()

#  Chart display
st.subheader("Token Transfer Volume Over Time")
if not chart_df.empty and {"timestamp", "total_volume", "token"}.issubset(chart_df.columns):
    fig = px.bar(chart_df, x="timestamp", y="total_volume", color="token", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No chart data available or missing expected columns.")

#  Search filter section
st.subheader("🔎 Filter Transfers")
if df.empty or not {"from_address", "to_address", "token"}.issubset(df.columns):
    st.warning("No transfer data available or required columns missing.")
    st.stop()

search = st.text_input("Search address or token...")
filtered_df = df[
    df["from_address"].str.contains(search, case=False, na=False) |
    df["to_address"].str.contains(search, case=False, na=False) |
    df["token"].str.contains(search, case=False, na=False)
]

st.dataframe(filtered_df, use_container_width=True)

#  Optional raw data viewer
if st.checkbox("Show raw API data"):
    st.json(df.to_dict(orient="records"))
