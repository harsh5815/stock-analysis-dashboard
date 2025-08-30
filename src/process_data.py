import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

os.makedirs("data/processed", exist_ok=True)

data = pd.read_csv("data/raw/stocks_raw.csv", header=[0,1],index_col=0,parse_dates = True)


close = data["Close"]
close.to_csv("data/processed/adj.close.csv")

returns = close.pct_change()
returns.to_csv("data/processed/daily_returns.csv")

cumulative_returns = (1 + returns).cumprod()
cumulative_returns.to_csv("data/processed/cumulative_returns.csv")

volatility = returns.std() * np.sqrt(252)
avg_returns = returns.mean() * 252
rf = 0.02
sharpe_ratio = (avg_returns -rf) / volatility

mertics = pd.DataFrame({
    "Annualized Return": avg_returns,
    "Annualized Volatility": volatility,
    "Sharpe_ratio": sharpe_ratio
})

drawdowns = {}
for ticker in close.columns:
    cum_return = (1 + returns[ticker].cumprod())
    rolling_max = cum_return.cummax()
    dd = cum_return / rolling_max - 1
    drawdowns[ticker] = dd

drawdowns_df = pd.DataFrame(drawdowns)
drawdowns_df.to_csv("data/processed/drawdowns.csv")

print("✅ Data processed and saved in data/processed/")

cumulative_returns.plot(figsize=(10,6))
plt.title("Cumulative Returns")
plt.xlabel("Date")
plt.ylabel("Growth of $1 Investment")
plt.legend(title="Ticker")
plt.grid(True)
plt.show()

# Plot daily returns
returns.plot(figsize=(10,6))
plt.title("Daily Returns")
plt.xlabel("Date")
plt.ylabel("Daily % Change")
plt.legend(title="Ticker")
plt.grid(True)
plt.show()