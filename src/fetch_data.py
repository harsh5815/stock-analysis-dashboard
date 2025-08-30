import yfinance as yf
import pandas as pd

tickers = ["AAPL","MSFT","TSLA"]
start = "2020-01-01"
end = "2025-01-01"

data = yf.download(tickers,start=start,end=end)

data.to_csv("data/raw/stocks_raw.csv")
print("Stock data downloaded and saved to data/raw/stocks_raw.csv")