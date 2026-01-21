import pandas as pd
import yfinance as yf
import os

os.environ['YF_ENABLE_CACHE'] = '0'

def fetch_crypto_data(symbol, period="5y"):
    """
    Fetch crypto data using yfinance (works on deployment)
    
    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'ETH', 'bitcoin', 'ethereum')
        period: Time period (default '5y')
    
    Returns:
        pandas.DataFrame: OHLCV data
    """
    name_to_symbol = {
        'bitcoin': 'BTC', 'ethereum': 'ETH', 'binancecoin': 'BNB',
        'ripple': 'XRP', 'cardano': 'ADA', 'dogecoin': 'DOGE',
        'solana': 'SOL', 'polkadot': 'DOT', 'polygon': 'MATIC',
        'litecoin': 'LTC', 'avalanche': 'AVAX', 'chainlink': 'LINK',
        'uniswap': 'UNI', 'cosmos': 'ATOM', 'stellar': 'XLM',
        'algorand': 'ALGO', 'vechain': 'VET', 'filecoin': 'FIL',
        'tron': 'TRX', 'near': 'NEAR', 'aptos': 'APT',
        'shiba-inu': 'SHIB', 'aave': 'AAVE', 'maker': 'MKR',
        'compound': 'COMP', 'curve': 'CRV', 'pancakeswap': 'CAKE',
        'sushiswap': 'SUSHI', 'arbitrum': 'ARB', 'optimism': 'OP'
    }
    
    ticker_symbol = name_to_symbol.get(symbol.lower(), symbol.upper())
    ticker = f"{ticker_symbol}-USD"
    
    try:
        crypto = yf.Ticker(ticker)
        df = crypto.history(period=period, progress=False, timeout=30)
        
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
