import yfinance as yf

def get_crypto_stats(symbol):
    """
    Get crypto statistics from yfinance
    
    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'ETH')
    
    Returns:
        dict: Crypto statistics
    """
    try:
        ticker = f"{symbol.upper()}-USD"
        crypto = yf.Ticker(ticker)
        info = crypto.info
        
        stats = {
            'symbol': symbol.upper(),
            'name': info.get('name', symbol),
            'current_price': info.get('regularMarketPrice', info.get('currentPrice', 'N/A')),
            'market_cap': info.get('marketCap', 'N/A'),
            'volume_24h': info.get('volume24Hr', info.get('volume', 'N/A')),
            'circulating_supply': info.get('circulatingSupply', 'N/A'),
            'total_supply': info.get('totalSupply', 'N/A'),
            'max_supply': info.get('maxSupply', 'N/A'),
            'day_high': info.get('dayHigh', 'N/A'),
            'day_low': info.get('dayLow', 'N/A'),
            'week_52_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'week_52_low': info.get('fiftyTwoWeekLow', 'N/A'),
            'price_change_24h': info.get('regularMarketChangePercent', 'N/A'),
            'ath': info.get('fiftyTwoWeekHigh', 'N/A'),
            'atl': info.get('fiftyTwoWeekLow', 'N/A')
        }
        
        return stats
        
    except Exception as e:
        return {
            'symbol': symbol.upper(),
            'error': str(e)
        }
