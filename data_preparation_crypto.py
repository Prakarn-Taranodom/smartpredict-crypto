import pandas as pd
from fetch_coinlore import fetch_crypto_data
from volatility_pipeline import compute_conditional_volatility

def get_crypto_markets():
    """Get available crypto markets/categories"""
    return {
        'top50': 'Top 50 Cryptocurrencies',
        'defi': 'DeFi Tokens',
        'layer1': 'Layer 1 Blockchains',
        'layer2': 'Layer 2 Solutions',
        'meme': 'Meme Coins'
    }

def get_market_cryptos(market):
    """Get crypto list for each market/category"""
    markets = {
        'top50': [
            'bitcoin', 'ethereum', 'binancecoin', 'ripple', 'cardano',
            'solana', 'polkadot', 'dogecoin', 'matic-network', 'litecoin',
            'avalanche-2', 'chainlink', 'uniswap', 'cosmos', 'stellar',
            'algorand', 'vechain', 'internet-computer', 'filecoin', 'tron',
            'ethereum-classic', 'near', 'aptos', 'arbitrum', 'optimism'
        ],
        'defi': [
            'uniswap', 'chainlink', 'aave', 'maker', 'compound',
            'curve-dao-token', 'pancakeswap-token', 'sushi', '1inch',
            'yearn-finance', 'synthetix-network-token', 'balancer', 'bancor'
        ],
        'layer1': [
            'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
            'polkadot', 'avalanche-2', 'cosmos', 'algorand', 'near',
            'aptos', 'sui', 'toncoin', 'hedera-hashgraph'
        ],
        'layer2': [
            'matic-network', 'arbitrum', 'optimism', 'immutable-x',
            'loopring', 'metis-token', 'boba-network'
        ],
        'meme': [
            'dogecoin', 'shiba-inu', 'pepe', 'floki', 'bonk',
            'baby-doge-coin', 'dogelon-mars', 'samoyedcoin'
        ]
    }
    return markets.get(market, markets['top50'])

def get_crypto_category(crypto_id):
    """Get category for a crypto"""
    categories = {
        'bitcoin': 'Layer 1', 'ethereum': 'Layer 1', 'binancecoin': 'Layer 1',
        'cardano': 'Layer 1', 'solana': 'Layer 1', 'polkadot': 'Layer 1',
        'avalanche-2': 'Layer 1', 'cosmos': 'Layer 1', 'algorand': 'Layer 1',
        'near': 'Layer 1', 'aptos': 'Layer 1',
        
        'matic-network': 'Layer 2', 'arbitrum': 'Layer 2', 'optimism': 'Layer 2',
        'immutable-x': 'Layer 2', 'loopring': 'Layer 2',
        
        'uniswap': 'DeFi', 'chainlink': 'DeFi', 'aave': 'DeFi',
        'maker': 'DeFi', 'compound': 'DeFi', 'curve-dao-token': 'DeFi',
        'pancakeswap-token': 'DeFi', 'sushi': 'DeFi',
        
        'dogecoin': 'Meme', 'shiba-inu': 'Meme', 'pepe': 'Meme',
        'floki': 'Meme', 'bonk': 'Meme',
        
        'ripple': 'Payment', 'stellar': 'Payment', 'litecoin': 'Payment',
        'tron': 'Payment', 'vechain': 'Supply Chain',
        'filecoin': 'Storage', 'internet-computer': 'Cloud Computing'
    }
    return categories.get(crypto_id, 'Other')

def prepare_crypto_data_for_clustering(cryptos, window_days=60, include_category=True):
    """Prepare crypto data for clustering"""
    cv_series_list = []
    total = len(cryptos)
    failed = []
    
    for idx, crypto in enumerate(cryptos, 1):
        try:
            print(f"[{idx}/{total}] Processing {crypto}...")
            
            df = fetch_crypto_data(crypto)
            if df is None or len(df) < window_days:
                print(f"Skipping {crypto}: insufficient data")
                failed.append(crypto)
                continue
            
            df_cv = compute_conditional_volatility(df)
            cv_series = df_cv['cv'].tail(window_days).values
            cv_normalized = (cv_series - cv_series.mean()) / cv_series.std()
            
            row_data = {'crypto_id': crypto}
            for i, cv_value in enumerate(cv_normalized):
                row_data[f'cv_t_{i+1}'] = cv_value
            
            if include_category:
                row_data['category'] = get_crypto_category(crypto)
            
            cv_series_list.append(row_data)
            print(f"✓ {crypto} processed")
            
        except Exception as e:
            print(f"✗ Skipping {crypto}: {str(e)[:50]}")
            failed.append(crypto)
            continue
    
    if not cv_series_list:
        raise ValueError(f"No valid cryptos. All {len(failed)} failed.")
    
    print(f"\n✓ Success: {len(cv_series_list)}/{total}")
    if failed:
        print(f"✗ Failed: {', '.join(failed[:10])}")
    
    cv_df = pd.DataFrame(cv_series_list)
    cv_df = cv_df.fillna(0)
    
    return cv_df

def prepare_market_data(market, window_days=60, include_category=True):
    """Prepare market data for clustering"""
    cryptos = get_market_cryptos(market)
    return prepare_crypto_data_for_clustering(cryptos, window_days, include_category)
