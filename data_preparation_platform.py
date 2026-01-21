import pandas as pd
from fetch_coinlore import fetch_crypto_data
from volatility_pipeline import compute_conditional_volatility

def get_crypto_platforms():
    """Get available blockchain platforms"""
    return {
        'ethereum': 'Ethereum Network',
        'bsc': 'Binance Smart Chain',
        'polygon': 'Polygon Network',
        'solana': 'Solana Network',
        'avalanche': 'Avalanche Network',
        'layer2': 'Layer 2 Solutions',
        'others': 'Other Chains'
    }

def get_crypto_sectors():
    """Get available crypto sectors from Coinlore"""
    return {
        'defi': 'DeFi (Decentralized Finance)',
        'nft': 'NFT & Metaverse',
        'gaming': 'Gaming & Play-to-Earn',
        'ai': 'AI & Big Data',
        'meme': 'Meme Coins',
        'exchange': 'Exchange Tokens',
        'stablecoin': 'Stablecoins',
        'layer1': 'Layer 1 Blockchains'
    }

def get_sector_cryptos(sector):
    """Get crypto list for each sector"""
    sectors = {
        'defi': [
            {'symbol': 'UNI', 'name': 'Uniswap'},
            {'symbol': 'AAVE', 'name': 'Aave'},
            {'symbol': 'MKR', 'name': 'Maker'},
            {'symbol': 'COMP', 'name': 'Compound'},
            {'symbol': 'CRV', 'name': 'Curve'},
            {'symbol': 'SNX', 'name': 'Synthetix'},
            {'symbol': 'LDO', 'name': 'Lido DAO'},
            {'symbol': 'SUSHI', 'name': 'SushiSwap'},
            {'symbol': 'CAKE', 'name': 'PancakeSwap'}
        ],
        'nft': [
            {'symbol': 'APE', 'name': 'ApeCoin'},
            {'symbol': 'SAND', 'name': 'The Sandbox'},
            {'symbol': 'MANA', 'name': 'Decentraland'},
            {'symbol': 'AXS', 'name': 'Axie Infinity'},
            {'symbol': 'GALA', 'name': 'Gala'}
        ],
        'gaming': [
            {'symbol': 'AXS', 'name': 'Axie Infinity'},
            {'symbol': 'SAND', 'name': 'The Sandbox'},
            {'symbol': 'MANA', 'name': 'Decentraland'},
            {'symbol': 'GALA', 'name': 'Gala'},
            {'symbol': 'IMX', 'name': 'Immutable X'}
        ],
        'ai': [
            {'symbol': 'FET', 'name': 'Fetch.ai'},
            {'symbol': 'OCEAN', 'name': 'Ocean Protocol'},
            {'symbol': 'GRT', 'name': 'The Graph'},
            {'symbol': 'RNDR', 'name': 'Render Token'}
        ],
        'meme': [
            {'symbol': 'DOGE', 'name': 'Dogecoin'},
            {'symbol': 'SHIB', 'name': 'Shiba Inu'},
            {'symbol': 'PEPE', 'name': 'Pepe'},
            {'symbol': 'FLOKI', 'name': 'Floki'}
        ],
        'exchange': [
            {'symbol': 'BNB', 'name': 'BNB'},
            {'symbol': 'UNI', 'name': 'Uniswap'},
            {'symbol': 'CAKE', 'name': 'PancakeSwap'},
            {'symbol': 'SUSHI', 'name': 'SushiSwap'}
        ],
        'stablecoin': [
            {'symbol': 'USDT', 'name': 'Tether'},
            {'symbol': 'USDC', 'name': 'USD Coin'},
            {'symbol': 'DAI', 'name': 'Dai'},
            {'symbol': 'BUSD', 'name': 'Binance USD'}
        ],
        'layer1': [
            {'symbol': 'BTC', 'name': 'Bitcoin'},
            {'symbol': 'ETH', 'name': 'Ethereum'},
            {'symbol': 'BNB', 'name': 'BNB'},
            {'symbol': 'SOL', 'name': 'Solana'},
            {'symbol': 'ADA', 'name': 'Cardano'},
            {'symbol': 'AVAX', 'name': 'Avalanche'},
            {'symbol': 'DOT', 'name': 'Polkadot'},
            {'symbol': 'MATIC', 'name': 'Polygon'},
            {'symbol': 'ATOM', 'name': 'Cosmos'},
            {'symbol': 'NEAR', 'name': 'NEAR Protocol'},
            {'symbol': 'APT', 'name': 'Aptos'}
        ]
    }
    return sectors.get(sector, [])

def get_platform_cryptos(platform):
    """Get crypto list for each platform - Top cryptos from Coinlore"""
    platforms = {
        'ethereum': [
            {'symbol': 'ETH', 'name': 'Ethereum'},
            {'symbol': 'USDT', 'name': 'Tether'},
            {'symbol': 'USDC', 'name': 'USD Coin'},
            {'symbol': 'UNI', 'name': 'Uniswap'},
            {'symbol': 'LINK', 'name': 'Chainlink'},
            {'symbol': 'AAVE', 'name': 'Aave'},
            {'symbol': 'MKR', 'name': 'Maker'},
            {'symbol': 'CRV', 'name': 'Curve'},
            {'symbol': 'SHIB', 'name': 'Shiba Inu'},
            {'symbol': 'COMP', 'name': 'Compound'},
            {'symbol': 'SNX', 'name': 'Synthetix'},
            {'symbol': 'LDO', 'name': 'Lido DAO'}
        ],
        'bsc': [
            {'symbol': 'BNB', 'name': 'BNB'},
            {'symbol': 'CAKE', 'name': 'PancakeSwap'},
            {'symbol': 'XVS', 'name': 'Venus'},
            {'symbol': 'ALPACA', 'name': 'Alpaca Finance'}
        ],
        'polygon': [
            {'symbol': 'MATIC', 'name': 'Polygon'},
            {'symbol': 'SUSHI', 'name': 'SushiSwap'}
        ],
        'solana': [
            {'symbol': 'SOL', 'name': 'Solana'},
            {'symbol': 'RAY', 'name': 'Raydium'},
            {'symbol': 'SRM', 'name': 'Serum'}
        ],
        'avalanche': [
            {'symbol': 'AVAX', 'name': 'Avalanche'},
            {'symbol': 'JOE', 'name': 'TraderJoe'}
        ],
        'layer2': [
            {'symbol': 'ARB', 'name': 'Arbitrum'},
            {'symbol': 'OP', 'name': 'Optimism'},
            {'symbol': 'IMX', 'name': 'Immutable X'}
        ],
        'others': [
            {'symbol': 'BTC', 'name': 'Bitcoin'},
            {'symbol': 'XRP', 'name': 'Ripple'},
            {'symbol': 'ADA', 'name': 'Cardano'},
            {'symbol': 'DOGE', 'name': 'Dogecoin'},
            {'symbol': 'DOT', 'name': 'Polkadot'},
            {'symbol': 'LTC', 'name': 'Litecoin'},
            {'symbol': 'TRX', 'name': 'Tron'},
            {'symbol': 'ATOM', 'name': 'Cosmos'},
            {'symbol': 'XLM', 'name': 'Stellar'},
            {'symbol': 'ALGO', 'name': 'Algorand'},
            {'symbol': 'VET', 'name': 'VeChain'},
            {'symbol': 'FIL', 'name': 'Filecoin'},
            {'symbol': 'NEAR', 'name': 'NEAR Protocol'},
            {'symbol': 'APT', 'name': 'Aptos'},
            {'symbol': 'ICP', 'name': 'Internet Computer'}
        ]
    }
    return platforms.get(platform, [])

def prepare_crypto_data_for_clustering(cryptos, window_days=60, include_platform=True):
    """Prepare crypto data for clustering"""
    cv_series_list = []
    total = len(cryptos)
    failed = []
    
    for idx, crypto in enumerate(cryptos, 1):
        try:
            symbol = crypto['symbol']
            platform = crypto.get('platform', 'Unknown')
            
            print(f"[{idx}/{total}] Processing {symbol}...")
            
            df = fetch_crypto_data(symbol)
            if df is None or len(df) < window_days:
                print(f"Skipping {symbol}: insufficient data")
                failed.append(symbol)
                continue
            
            df_cv = compute_conditional_volatility(df)
            cv_series = df_cv['cv'].tail(window_days).values
            cv_normalized = (cv_series - cv_series.mean()) / cv_series.std()
            
            row_data = {'crypto_id': symbol}
            for i, cv_value in enumerate(cv_normalized):
                row_data[f'cv_t_{i+1}'] = cv_value
            
            if include_platform:
                row_data['category'] = platform
            
            cv_series_list.append(row_data)
            print(f"✓ {symbol} processed")
            
        except Exception as e:
            print(f"✗ Skipping {crypto['symbol']}: {str(e)[:50]}")
            failed.append(crypto['symbol'])
            continue
    
    if not cv_series_list:
        raise ValueError(f"No valid cryptos. All {len(failed)} failed.")
    
    print(f"\n✓ Success: {len(cv_series_list)}/{total}")
    if failed:
        print(f"✗ Failed: {', '.join(failed[:10])}")
    
    cv_df = pd.DataFrame(cv_series_list)
    cv_df = cv_df.fillna(0)
    
    return cv_df

def prepare_platform_data(platform, window_days=60, include_platform=True):
    """Prepare platform data for clustering"""
    cryptos = get_platform_cryptos(platform)
    
    for crypto in cryptos:
        crypto['platform'] = platform.title()
    
    return prepare_crypto_data_for_clustering(cryptos, window_days, include_platform)
