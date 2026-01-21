import requests

def get_crypto_stats(symbol):
    """
    Get crypto statistics from CoinLore API
    
    Args:
        symbol: Crypto symbol (e.g., 'BTC', 'ETH')
    
    Returns:
        dict: Crypto statistics
    """
    try:
        # Get all tickers from CoinLore
        url = "https://api.coinlore.net/api/tickers/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Find the crypto by symbol
        crypto_data = None
        for crypto in data.get('data', []):
            if crypto.get('symbol', '').upper() == symbol.upper():
                crypto_data = crypto
                break
        
        if not crypto_data:
            return {
                'symbol': symbol.upper(),
                'error': 'Crypto not found'
            }
        
        stats = {
            'symbol': crypto_data.get('symbol', symbol.upper()),
            'name': crypto_data.get('name', symbol),
            'current_price': float(crypto_data.get('price_usd', 0)),
            'market_cap': float(crypto_data.get('market_cap_usd', 0)),
            'volume_24h': float(crypto_data.get('volume24', 0)),
            'circulating_supply': float(crypto_data.get('csupply', 0)),
            'total_supply': float(crypto_data.get('tsupply', 0)),
            'max_supply': float(crypto_data.get('msupply', 0)) if crypto_data.get('msupply') else 'N/A',
            'price_change_24h': float(crypto_data.get('percent_change_24h', 0)),
            'rank': crypto_data.get('rank', 'N/A')
        }
        
        return stats
        
    except Exception as e:
        return {
            'symbol': symbol.upper(),
            'error': str(e)
        }
