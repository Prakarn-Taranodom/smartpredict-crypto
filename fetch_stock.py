import pandas as pd
import requests
import os
from datetime import datetime, timedelta

def fetch_stock_data(ticker, period="5y"):
    """
    Fetch stock data using Finnhub API (supports US and Thai stocks).
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'AOT.BK')
        period: Time period ('5y', '1y', '6mo')
    
    Returns:
        pandas.DataFrame: Stock data with Date index and OHLCV columns
    """
    api_key = os.getenv('FINNHUB_API_KEY')
    
    if not api_key:
        raise ValueError(
            "FINNHUB_API_KEY not found. "
            "Get free key at https://finnhub.io/register "
            "Then set in Render: Environment → FINNHUB_API_KEY"
        )
    
    # Convert period to timestamps
    end_date = datetime.now()
    if period == "5y":
        start_date = end_date - timedelta(days=5*365)
    elif period == "1y":
        start_date = end_date - timedelta(days=365)
    elif period == "6mo":
        start_date = end_date - timedelta(days=180)
    else:
        start_date = end_date - timedelta(days=5*365)
    
    # Convert .BK to Bangkok exchange format
    if ticker.endswith('.BK'):
        ticker = ticker.replace('.BK', '.BK')  # Finnhub uses same format
    
    # Finnhub API endpoint
    url = "https://finnhub.io/api/v1/stock/candle"
    params = {
        "symbol": ticker,
        "resolution": "D",  # Daily data
        "from": int(start_date.timestamp()),
        "to": int(end_date.timestamp()),
        "token": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Check for errors
        if data.get('s') == 'no_data':
            raise ValueError(f"No data found for {ticker}. Check ticker symbol.")
        
        if 'c' not in data or not data['c']:
            raise ValueError(f"Invalid response for {ticker}: {data}")
        
        # Convert to DataFrame
        df = pd.DataFrame({
            'Open': data['o'],
            'High': data['h'],
            'Low': data['l'],
            'Close': data['c'],
            'Volume': data['v']
        })
        
        # Convert timestamps to datetime index
        df.index = pd.to_datetime(data['t'], unit='s')
        df = df.sort_index()
        
        if len(df) < 30:
            raise ValueError(f"{ticker}: Only {len(df)} days of data (need 30+)")
        
        return df
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error fetching {ticker}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to fetch {ticker}: {str(e)}")
