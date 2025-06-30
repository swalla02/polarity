import streamlit as st
import requests
from datetime import datetime
import pandas as pd

API_BASE_URL = "http://localhost:1234/api/v1/comments_polarity"

st.title("📊 Feddit Comment Polarity Viewer")

mode = st.radio("Choose mode:", ["🔢 By Limit", "🕒 By Time Range"])
feddit_name = st.text_input("Enter Feddit Name :")
sort_order = st.selectbox("Sort by polarity:", ["Descending", "Ascending"])

if mode == "🔢 By Limit":
    limit = st.slider("Number of comments to fetch:",
                      min_value=1, max_value=25, value=10)
    if st.button("Fetch Comments"):
        if not feddit_name:
            st.warning("Please enter a Feddit name.")
        else:
            with st.spinner("Fetching comments..."):
                payload = {
                    "feddit_name": feddit_name,
                    "limit": limit
                }
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/limit", json=payload)
                    response.raise_for_status()
                    comments = response.json().get("comments", [])
                    df = pd.DataFrame(comments)
                    df.set_index("id", inplace=True)
                    df = df.sort_values("polarity_score", ascending=(
                        sort_order == "Ascending"))
                    st.dataframe(
                        df[["text", "polarity", "polarity_score"]], use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

else:
    start_time = st.date_input("Start Date", value=datetime(2023, 1, 1))
    end_time = st.date_input("End Date", value=datetime.now().date())
    if st.button("Fetch Comments"):
        if not feddit_name:
            st.warning("Please enter a Feddit name.")
        elif start_time >= end_time:
            st.warning("Start date must be before end date.")
        else:
            with st.spinner("Fetching comments within time range..."):
                payload = {
                    "feddit_name": feddit_name,
                    "time_range": [
                        datetime.combine(
                            start_time, datetime.min.time()).isoformat(),
                        datetime.combine(
                            end_time, datetime.min.time()).isoformat()
                    ]
                }
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/with_time", json=payload)
                    response.raise_for_status()
                    comments = response.json().get("comments_with_time", [])
                    df = pd.DataFrame(comments)
                    df.set_index("id", inplace=True)
                    df["created_at"] = pd.to_datetime(df["created_at"])
                    df = df.sort_values("polarity_score", ascending=(
                        sort_order == "Ascending"))
                    st.dataframe(
                        df[["created_at", "text", "polarity", "polarity_score"]], use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
