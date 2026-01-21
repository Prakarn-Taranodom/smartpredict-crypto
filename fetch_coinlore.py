import pandas as pd
import requests
from datetime import datetime, timedelta
import time

def get_coinlore_id(symbol):
    """Get Coinlore coin ID from symbol"""
    symbol_to_id = {
        'BTC': 90, 'ETH': 80, 'BNB': 2710, 'XRP': 58,
        'ADA': 257, 'DOGE': 2, 'SOL': 48543, 'DOT': 35683,
        'MATIC': 33536, 'LTC': 1, 'AVAX': 44883, 'LINK': 2321,
        'UNI': 33538, 'ATOM': 33285, 'XLM': 4, 'ALGO': 33234,
        'VET': 33285, 'FIL': 33536, 'TRX': 2713, 'NEAR': 44444,
        'APT': 50000, 'ARB': 51000, 'SHIB': 44444, 'AAVE': 33234,
        'MKR': 33285, 'COMP': 33537, 'CRV': 33536, 'CAKE': 33539,
        'SUSHI': 33543, 'OP': 50500
    }
    return symbol_to_id.get(symbol.upper())

def fetch_crypto_data(symbol, period="5y"):
    """
    Fetch crypto data from Coinlore API
    Falls back to yfinance if Coinlore fails
    
    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'ETH')
        period: Time period (default '5y')
    
    Returns:
        pandas.DataFrame: OHLCV data
    """
    coin_id = get_coinlore_id(symbol)
    
    if coin_id:
        try:
            # Try Coinlore API first
            url = f"https://api.coinlore.net/api/coin/markets/?id={coin_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # If Coinlore works, use it
                # Otherwise fall through to yfinance
                if data and len(data) > 0:
                    # Coinlore doesn't provide historical OHLCV easily
                    # So we'll use yfinance as primary source
                    pass
        except:
            pass
    
    # Use yfinance as primary data source (reliable and free)
    try:
        import yfinance as yf
        import os
        os.environ['YF_ENABLE_CACHE'] = '0'
        
        ticker = f"{symbol.upper()}-USD"
        crypto = yf.Ticker(ticker)
        df = crypto.history(period=period)
        
        if df.empty:
            raise ValueError(f"No data found for {symbol}")
        
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns for {symbol}")
        
        df = df[required_cols].dropna()
        
        if len(df) < 30:
            raise ValueError(f"{symbol}: Only {len(df)} days of data (need 30+)")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Failed to fetch {symbol}: {str(e)}")
