import numpy as np
import datetime as dt
import pandas_datareader as pdr
import pandas as pd
import yfinance as yf

# creates list of tickers
tickers = ['^GSPC']
number_of_tickers = int(input("How many stocks in your portfolio? "))

for x in range(number_of_tickers):
    tickers.append(input("What ticker do you want to add to your portfolio? ").upper())

# gather data
start = dt.datetime(2011, 12, 1)
end = dt.datetime(2022, 6, 1)

data = pdr.get_data_yahoo(tickers, start, end, interval='d')
data = data["Adj Close"]

# compute beta and returns
log_returns = np.log(data/data.shift())

cov = log_returns.cov()
var = log_returns['^GSPC'].var()

beta = cov.loc['AAPL', '^GSPC']/var

risk_free_rate = (yf.Ticker('^TNX').info['regularMarketPreviousClose'] / 100)
market_return = .105

expected_return = risk_free_rate + beta * (market_return - risk_free_rate)

beta = (cov.loc['^GSPC'] / var).round(2)

market_return = (risk_free_rate + beta * (market_return - risk_free_rate) * 100).round(2)

data_tuples = list(zip(tickers, beta, market_return))

summary = pd.DataFrame(data_tuples, columns=['Ticker', 'Beta', 'Return'])

# print tickers, beta, and returns
print(summary)
