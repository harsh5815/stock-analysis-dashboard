import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px

# ---------------------------
# APP TITLE
# ---------------------------
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")
st.title("📊 Stock Market Analysis Dashboard")
st.markdown("Analyze stock performance, returns, and risk metrics interactively.")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("⚙️ Filter Options")

tickers = st.sidebar.multiselect(
    "Select stocks:",
    ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN"],
    default=["AAPL", "MSFT"]
)

start = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end = st.sidebar.date_input("End Date", pd.to_datetime("2025-01-01"))

# ---------------------------
# FETCH DATA
# ---------------------------
if tickers:
    data = yf.download(tickers, start=start, end=end)
    close = data["Close"]
    returns = close.pct_change()
    cumulative_returns = (1 + returns).cumprod()

    # ---------------------------
    # SHOW DATA
    # ---------------------------
    st.subheader("📂 Latest Data Snapshot")
    st.dataframe(close.tail())

    # ---------------------------
    # KPIs (Key Metrics)
    # ---------------------------
    st.subheader("📈 Risk Metrics")
    volatility = returns.std() * np.sqrt(252)
    avg_return = returns.mean() * 252
    sharpe_ratio = (avg_return - 0.02) / volatility

    col1, col2, col3 = st.columns(3)
    col1.metric("Volatility", f"{volatility.mean():.2%}")
    col2.metric("Avg Annual Return", f"{avg_return.mean():.2%}")
    col3.metric("Sharpe Ratio", f"{sharpe_ratio.mean():.2f}")

    # ---------------------------
    # CHARTS
    # ---------------------------

    # Cumulative Returns Plot
    st.subheader("📊 Cumulative Returns Over Time")
    fig_cum = px.line(cumulative_returns, title="Cumulative Returns", labels={"value": "Growth of $1 Investment"})
    st.plotly_chart(fig_cum, use_container_width=True)

    # Daily Returns Plot
    st.subheader("📉 Daily Returns Over Time")
    fig_ret = px.line(returns, title="Daily Returns", labels={"value": "Daily % Change"})
    st.plotly_chart(fig_ret, use_container_width=True)

    # Distribution of Returns
    st.subheader("📊 Distribution of Daily Returns")
    fig_hist = px.histogram(returns, nbins=50, title="Return Distribution", marginal="box")
    st.plotly_chart(fig_hist, use_container_width=True)
