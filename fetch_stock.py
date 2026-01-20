import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker):
    df = yf.download(ticker, period="5y")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df

