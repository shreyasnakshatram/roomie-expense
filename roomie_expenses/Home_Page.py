# app_no_session_state.py
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

# SQLAlchemy imports if you want real DB
# from sqlalchemy import func
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from models import User, Expense

st.set_page_config(page_title="Expenses by User (no session_state)", layout="wide")
st.title("Expenses by User (no session_state)")

# Helper: Replace with your actual session factory
def get_session():
    # from database import SessionLocal
    # return SessionLocal()
    return None

def load_user_totals(session) -> pd.DataFrame:
    """
    Returns DataFrame with: user_id, name, total_amount, num_expenses
    Replace the demo block with a SQLAlchemy query when wiring to DB.
    """
    sample = [
        {"user_id": 1, "name": "Alice", "total_amount": 345.5, "num_expenses": 3},
        {"user_id": 2, "name": "Bob",   "total_amount": 1200.0, "num_expenses": 5},
        {"user_id": 3, "name": "Cara",  "total_amount": 75.0, "num_expenses": 1},
    ]
    return pd.DataFrame(sample)

def load_expenses(session) -> pd.DataFrame:
    """Return all expenses as DataFrame. Replace demo with DB query."""
    sample = [
        {"id": 1, "source_of_expense": "Office Supplies", "amount": 100.0, "added_by_id": 1, "month": "Dec", "year": 2025, "created_at": datetime.utcnow()},
        {"id": 2, "source_of_expense": "Team Lunch", "amount": 245.5, "added_by_id": 1, "month": "Dec", "year": 2025, "created_at": datetime.utcnow()},
        {"id": 3, "source_of_expense": "Laptop repairs", "amount": 1200.0, "added_by_id": 2, "month": "Nov", "year": 2025, "created_at": datetime.utcnow()},
        {"id": 4, "source_of_expense": "Taxi", "amount": 75.0, "added_by_id": 3, "month": "Dec", "year": 2025, "created_at": datetime.utcnow()},
        {"id": 5, "source_of_expense": "Snacks", "amount": 0.0, "added_by_id": 2, "month": "Dec", "year": 2025, "created_at": datetime.utcnow()},
    ]
    return pd.DataFrame(sample)

# Option to use real DB (if wired)
use_db = st.checkbox("Use real DB (uncheck to use demo data)", value=False)
session = None
if use_db:
    session = get_session()

try:
    user_totals = load_user_totals(session)
    expenses_df = load_expenses(session)
finally:
    if use_db and session is not None:
        session.close()

if user_totals.empty:
    st.info("No users found.")
    st.stop()

# Read selected user from query params (no session_state)
query_params = st.experimental_get_query_params()
selected_user_id = None
if "selected_user" in query_params:
    try:
        selected_user_id = int(query_params["selected_user"][0])
    except Exception:
        selected_user_id = None

# UI: show columns for users
max_columns_in_row = 6
users = user_totals.to_dict(orient="records")

for i in range(0, len(users), max_columns_in_row):
    row_users = users[i : i + max_columns_in_row]
    cols = st.columns(len(row_users))
    for col, user in zip(cols, row_users):
        with col:
            # Highlight selected by showing different header text
            header = f"{user['name']}"
            if selected_user_id == int(user["user_id"]):
                header = f"👉 {header}"
            st.metric(label=header, value=f"₹{user['total_amount']:.2f}", delta=f"{user['num_expenses']}")

            # Button sets query param (no session_state)
            btn_key = f"select_user_{user['user_id']}"
            if st.button("Show expenses", key=btn_key):
                # set selected_user in URL query params; this triggers rerun
                st.experimental_set_query_params(selected_user=str(user["user_id"]))

st.markdown("---")

if selected_user_id is None:
    st.info("Click *Show expenses* on any user to see their expenses below. (Selection stored in URL query params.)")
else:
    st.subheader(f"Expenses by user id: {selected_user_id}")
    filtered = expenses_df[expenses_df["added_by_id"] == int(selected_user_id)].copy()
    if filtered.empty:
        st.warning("No expenses found for this user.")
    else:
        # Format created_at nicely
        if "created_at" in filtered.columns:
            filtered["created_at"] = pd.to_datetime(filtered["created_at"])
            filtered["created_at"] = filtered["created_at"].dt.strftime("%Y-%m-%d %H:%M:%S")
        st.dataframe(filtered.sort_values(by="created_at", ascending=False), use_container_width=True)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"user_{selected_user_id}_expenses.csv",
            mime="text/csv",
        )
