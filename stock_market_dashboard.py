import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# Title
st.title("📊 Live Stock Market Dashboard")

# Sidebar
st.sidebar.header("Filter Options")

# Stock options
stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS']
selected_stock = st.sidebar.selectbox("Select a stock:", stocks)

# Date range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2024-12-31'))

# Download the stock data
ticker = yf.Tickers(selected_stock)
data = ticker.history(start=start_date, end=end_date)

# 🛠 Fix the columns for MultiIndex
data.columns = ['_'.join(col).strip() for col in data.columns.values]

# Example: Column names will become 'Close_RELIANCE.NS', 'Open_RELIANCE.NS', etc.

# Show data
st.subheader(f"Raw Data for {selected_stock}")
st.dataframe(data)

# Closing Price Chart
st.subheader("Closing Price Over Time")
fig_close = px.line(data, x=data.index, y=f'Close_{selected_stock}', title=f'{selected_stock} Closing Price')
st.plotly_chart(fig_close)

# Volume Chart
st.subheader("Volume Traded Over Time")
fig_volume = px.bar(data, x=data.index, y=f'Volume_{selected_stock}', title=f'{selected_stock} Volume Traded')
st.plotly_chart(fig_volume)

# Moving Average
st.subheader("Moving Average (30 Days)")
data[f'MA30_{selected_stock}'] = data[f'Close_{selected_stock}'].rolling(window=30).mean()
fig_ma = px.line(data, x=data.index, y=[f'Close_{selected_stock}', f'MA30_{selected_stock}'], title=f'{selected_stock} 30-Day Moving Average')
st.plotly_chart(fig_ma)

# Summary Statistics
st.subheader("Summary Statistics")
st.write(data.describe())
