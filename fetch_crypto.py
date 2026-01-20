import pandas as pd
import requests
from datetime import datetime

def fetch_crypto_data(symbol, period="5y"):
    """
    Fetch cryptocurrency data using CoinGecko API (free, no API key needed).
    
    Args:
        symbol: Crypto symbol (e.g., 'bitcoin', 'ethereum', 'BTC', 'ETH')
        period: Time period ('5y', '1y', '6mo')
    
    Returns:
        pandas.DataFrame: Crypto data with Date index and OHLCV columns
    """
    # Convert common symbols to CoinGecko IDs
    symbol_map = {
        'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binancecoin',
        'XRP': 'ripple', 'ADA': 'cardano', 'DOGE': 'dogecoin',
        'SOL': 'solana', 'DOT': 'polkadot', 'MATIC': 'matic-network',
        'LTC': 'litecoin', 'AVAX': 'avalanche-2', 'LINK': 'chainlink',
        'UNI': 'uniswap', 'ATOM': 'cosmos', 'XLM': 'stellar',
        'ALGO': 'algorand', 'VET': 'vechain', 'ICP': 'internet-computer',
        'FIL': 'filecoin', 'TRX': 'tron', 'ETC': 'ethereum-classic',
        'NEAR': 'near', 'APT': 'aptos', 'ARB': 'arbitrum'
    }
    
    # Convert to CoinGecko ID
    coin_id = symbol_map.get(symbol.upper(), symbol.lower())
    
    # Convert period to days
    days_map = {'5y': 1825, '1y': 365, '6mo': 180, '3mo': 90, '1mo': 30}
    days = days_map.get(period, 1825)
    
    # CoinGecko API endpoint
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'prices' not in data:
            raise ValueError(f"No data found for {symbol}")
        
        # Parse data
        prices = data['prices']
        volumes = data.get('total_volumes', [])
        
        # Create DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'Close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Add volume
        if volumes:
            vol_df = pd.DataFrame(volumes, columns=['timestamp', 'Volume'])
            vol_df['timestamp'] = pd.to_datetime(vol_df['timestamp'], unit='ms')
            vol_df.set_index('timestamp', inplace=True)
            df = df.join(vol_df)
        else:
            df['Volume'] = 0
        
        # Create OHLC from Close (approximation)
        df['Open'] = df['Close'].shift(1).fillna(df['Close'])
        df['High'] = df['Close'] * 1.02
        df['Low'] = df['Close'] * 0.98
        
        # Reorder columns
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        if len(df) < 30:
            raise ValueError(f"{symbol}: Only {len(df)} days of data (need 30+)")
        
        return df
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Network error fetching {symbol}: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to fetch {symbol}: {str(e)}")
