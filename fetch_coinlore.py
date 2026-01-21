import pandas as pd
import requests
from datetime import datetime, timedelta
import time

def fetch_crypto_data(symbol, period="5y"):
    """
    Fetch crypto data from CoinGecko API (free, no API key needed)
    
    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'ETH')
        period: Time period (default '5y')
    
    Returns:
        pandas.DataFrame: OHLCV data
    """
    symbol_to_id = {
        'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binancecoin', 'XRP': 'ripple',
        'ADA': 'cardano', 'DOGE': 'dogecoin', 'SOL': 'solana', 'DOT': 'polkadot',
        'MATIC': 'matic-network', 'LTC': 'litecoin', 'AVAX': 'avalanche-2', 'LINK': 'chainlink',
        'UNI': 'uniswap', 'ATOM': 'cosmos', 'XLM': 'stellar', 'ALGO': 'algorand',
        'VET': 'vechain', 'FIL': 'filecoin', 'TRX': 'tron', 'NEAR': 'near',
        'APT': 'aptos', 'ARB': 'arbitrum', 'SHIB': 'shiba-inu', 'AAVE': 'aave',
        'MKR': 'maker', 'COMP': 'compound-governance-token', 'CRV': 'curve-dao-token',
        'CAKE': 'pancakeswap-token', 'SUSHI': 'sushi', 'OP': 'optimism',
        'USDT': 'tether', 'USDC': 'usd-coin', 'DAI': 'dai', 'BUSD': 'binance-usd',
        'SNX': 'synthetix-network-token', 'LDO': 'lido-dao', 'XVS': 'venus',
        'ALPACA': 'alpaca-finance', 'RAY': 'raydium', 'SRM': 'serum',
        'JOE': 'joe', 'IMX': 'immutable-x', 'APE': 'apecoin',
        'SAND': 'the-sandbox', 'MANA': 'decentraland', 'AXS': 'axie-infinity',
        'GALA': 'gala', 'FET': 'fetch-ai', 'OCEAN': 'ocean-protocol',
        'GRT': 'the-graph', 'RNDR': 'render-token', 'PEPE': 'pepe',
        'FLOKI': 'floki', 'ICP': 'internet-computer'
    }
    
    coin_id = symbol_to_id.get(symbol.upper())
    if not coin_id:
        raise ValueError(f"Unsupported crypto: {symbol}")
    
    try:
        # Calculate days based on period
        days_map = {'1y': 365, '2y': 730, '5y': 1825, '6mo': 180, '3mo': 90}
        days = days_map.get(period, 1825)
        
        # Fetch from CoinGecko
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {'vs_currency': 'usd', 'days': days, 'interval': 'daily'}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Parse data
        prices = data.get('prices', [])
        volumes = data.get('total_volumes', [])
        
        if not prices or len(prices) < 30:
            raise ValueError(f"{symbol}: Insufficient data")
        
        # Create DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'Close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Add volume
        vol_df = pd.DataFrame(volumes, columns=['timestamp', 'Volume'])
        vol_df['timestamp'] = pd.to_datetime(vol_df['timestamp'], unit='ms')
        vol_df.set_index('timestamp', inplace=True)
        df['Volume'] = vol_df['Volume']
        
        # Create OHLC from Close (approximation)
        df['Open'] = df['Close']
        df['High'] = df['Close'] * 1.02
        df['Low'] = df['Close'] * 0.98
        
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
        
        return df
        
    except Exception as e:
        raise ValueError(f"Failed to fetch {symbol}: {str(e)}")
