import yfinance as yf
import pandas as pd
import time

def fetch_stock_data(ticker, period="5y", max_retries=3):
    # Set User-Agent to avoid being blocked
    yf.pdr_override()
    
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            
            if df.empty:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"No data found for {ticker}")
            
            if len(df) < 30:
                raise ValueError(f"{ticker}: Only {len(df)} days of data (need 30+)")
            
            return df
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise ValueError(f"Failed to fetch {ticker}: {str(e)}")
