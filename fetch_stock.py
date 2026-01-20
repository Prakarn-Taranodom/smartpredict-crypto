import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period="5y"):
    """
    Fetch stock data using yfinance (works on Render with proper settings).
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'AOT.BK')
        period: Time period ('5y', '1y', '6mo')
    
    Returns:
        pandas.DataFrame: Stock data with Date index and OHLCV columns
    """
    try:
        # Download data with yfinance
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            raise ValueError(f"No data found for {ticker}")
        
        # Ensure we have the required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns for {ticker}")
        
        # Keep only OHLCV columns
        df = df[required_cols]
        
        if len(df) < 30:
            raise ValueError(f"{ticker}: Only {len(df)} days of data (need 30+)")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Failed to fetch {ticker}: {str(e)}")
