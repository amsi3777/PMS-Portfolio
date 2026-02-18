import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(
    page_title="PMS-GRADE PORTFOLIO TRACKER",
    layout="wide",
)

st.title("📊 PMS-GRADE PORTFOLIO TRACKER")
st.caption("Feb 2026 Master Version – Streamlit Edition")

# =============================
# LOAD NSE MASTER
# =============================
@st.cache_data
def load_master():
    return pd.read_csv("stock_master_nse_jan2026.csv")

try:
    master_df = load_master()
except:
    st.warning("Upload NSE Master CSV in project folder.")

# =============================
# SIDEBAR
# =============================
st.sidebar.header("⚙ Portfolio Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Existing Portfolio CSV",
    type=["csv"]
)

manual_entry = st.sidebar.radio(
    "Add Manual Transactions?",
    ["No", "Yes"]
)

# =============================
# MANUAL ENTRY SECTION
# =============================
transactions = []

if manual_entry == "Yes":

    st.sidebar.subheader("➕ Add Transaction")

    search_text = st.sidebar.text_input("Search Stock (Type 2-3 letters)")

    if search_text:
        filtered = master_df[
            master_df["SYMBOL"].str.contains(search_text.upper(), na=False)
        ]
        stock_list = filtered["SYMBOL"].tolist()
    else:
        stock_list = []

    selected_stock = st.sidebar.selectbox("Select Stock", stock_list)

    date = st.sidebar.date_input("Date")
    qty = st.sidebar.number_input("Quantity", min_value=0)
    price = st.sidebar.number_input("Price", min_value=0.0)
    txn_type = st.sidebar.selectbox("Type", ["BUY", "SELL"])

    if st.sidebar.button("Add Transaction"):
        transactions.append(
            [date, selected_stock, qty, price, txn_type]
        )
        st.sidebar.success("Added!")

# =============================
# PROCESS DATA
# =============================
if uploaded_file:
    portfolio_df = pd.read_csv(uploaded_file)
else:
    portfolio_df = pd.DataFrame(
        transactions,
        columns=["Date", "Symbol", "Quantity", "Price", "Type"]
    )

if not portfolio_df.empty:

    st.subheader("📈 Portfolio Summary")

    total_investment = (portfolio_df["Quantity"] * portfolio_df["Price"]).sum()
    current_value = total_investment  # Placeholder
    realised = 0
    unrealised = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Investment", f"₹{total_investment:,.2f}")
    col2.metric("Current Value", f"₹{current_value:,.2f}")
    col3.metric("Realised P/L", f"₹{realised:,.2f}")
    col4.metric("Unrealised P/L", f"₹{unrealised:,.2f}")

    st.subheader("📜 Ledger")
    st.dataframe(portfolio_df, use_container_width=True)

    # SAVE BUTTON
    st.subheader("💾 Save Portfolio")

    if st.button("Save Portfolio"):
        filename = f"Equity_Portfolio_Tracker_{datetime.datetime.now().strftime('%d%m%Y_%H%M%S')}.csv"
        portfolio_df.to_csv(filename, index=False)
        st.success(f"Saved as {filename}")
