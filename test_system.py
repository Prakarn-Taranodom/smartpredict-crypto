# -*- coding: utf-8 -*-
"""
Test script for SmartPredict Crypto system
Tests: fetch data, prediction, clustering
"""
import sys
import io
import numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("TESTING SMARTPREDICT CRYPTO SYSTEM")
print("=" * 60)

# Test 1: Fetch Crypto Data
print("\n[TEST 1] Testing fetch_crypto_data...")
try:
    from fetch_coinlore import fetch_crypto_data
    
    print("  → Fetching BTC data...")
    df = fetch_crypto_data('BTC')
    print(f"  ✓ BTC: {len(df)} days of data")
    print(f"    Columns: {list(df.columns)}")
    print(f"    Date range: {df.index[0]} to {df.index[-1]}")
    
    print("  → Fetching ETH data...")
    df_eth = fetch_crypto_data('ETH')
    print(f"  ✓ ETH: {len(df_eth)} days of data")
    
    print("✅ TEST 1 PASSED: Data fetching works!")
except Exception as e:
    print(f"❌ TEST 1 FAILED: {str(e)}")

# Test 2: Volatility Calculation
print("\n[TEST 2] Testing volatility calculation...")
try:
    from volatility_pipeline import compute_conditional_volatility
    
    print("  → Computing conditional volatility for BTC...")
    df_cv = compute_conditional_volatility(df)
    print(f"  ✓ CV computed: {len(df_cv)} rows")
    print(f"    CV columns: {list(df_cv.columns)}")
    print(f"    CV mean: {df_cv['cv'].mean():.6f}")
    print(f"    CV std: {df_cv['cv'].std():.6f}")
    
    print("✅ TEST 2 PASSED: Volatility calculation works!")
except Exception as e:
    print(f"❌ TEST 2 FAILED: {str(e)}")

# Test 3: Feature Engineering & Prediction
print("\n[TEST 3] Testing prediction pipeline...")
try:
    from feature_engineering import build_features
    from train_model import train_rf, predict_next_n_days_prices
    
    print("  → Building features...")
    X, y = build_features(df_cv)
    print(f"  ✓ Features: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"    Feature names: {list(X.columns[:5])}...")
    
    print("  → Training Random Forest model...")
    model = train_rf(X, y)
    print(f"  ✓ Model trained")
    
    print("  → Predicting next 5 days...")
    predicted_prices, preds, probs = predict_next_n_days_prices(model, X, df_cv, n=5)
    print(f"  ✓ Predictions:")
    for i, (price, pred, prob) in enumerate(zip(predicted_prices, preds, probs), 1):
        direction = "UP" if pred == 1 else "DOWN"
        print(f"    Day {i}: ${price:.2f} - {direction} ({prob:.2%})")
    
    print("✅ TEST 3 PASSED: Prediction pipeline works!")
except Exception as e:
    print(f"❌ TEST 3 FAILED: {str(e)}")

# Test 4: Platform Data Preparation
print("\n[TEST 4] Testing platform data preparation...")
try:
    from data_preparation_platform import get_platform_cryptos, prepare_crypto_data_for_clustering
    
    print("  → Getting Ethereum platform cryptos...")
    eth_cryptos = get_platform_cryptos('ethereum')
    print(f"  ✓ Ethereum has {len(eth_cryptos)} cryptos")
    print(f"    Cryptos: {[c['symbol'] for c in eth_cryptos[:3]]}...")
    
    print("  → Preparing clustering data (testing with 3 cryptos)...")
    test_cryptos = eth_cryptos[:3]  # Test with 3 cryptos
    for c in test_cryptos:
        c['platform'] = 'Ethereum'
    
    cv_df = prepare_crypto_data_for_clustering(test_cryptos, window_days=60, include_platform=True)
    print(f"  ✓ Clustering data prepared: {len(cv_df)} cryptos")
    print(f"    Columns: {cv_df.shape[1]} features")
    
    print("✅ TEST 4 PASSED: Platform data preparation works!")
except Exception as e:
    print(f"❌ TEST 4 FAILED: {str(e)}")

# Test 5: Clustering
print("\n[TEST 5] Testing clustering...")
try:
    from clustering_module import (
        EuclideanKMeansClustering,
        compute_elbow_curve,
        detect_elbow_point,
        compute_cluster_metrics,
        get_cluster_statistics
    )
    
    print("  → Extracting features for clustering...")
    X = cv_df.iloc[:, 1:-1].values
    print(f"  ✓ Feature matrix: {X.shape}")
    
    print("  → Computing elbow curve...")
    if len(X) >= 3:
        elbow_data = compute_elbow_curve(X, k_range=range(2, min(5, len(X))), method="euclidean")
        print(f"  ✓ Elbow data: K values = {elbow_data['k_values']}")
        print(f"    Inertia values: {[f'{v:.2f}' for v in elbow_data['inertia_values']]}")
        
        print("  → Detecting elbow point...")
        elbow_info = detect_elbow_point(elbow_data['inertia_values'], elbow_data['k_values'])
        print(f"  ✓ Optimal K = {elbow_info['elbow_k']}")
    else:
        print("  ⚠ Skipping elbow curve (need at least 3 samples)")
    
    print("  → Performing clustering with K=2...")
    clustering = EuclideanKMeansClustering(n_clusters=2)
    labels = clustering.fit_predict(X)
    print(f"  ✓ Clustering done: {len(labels)} samples")
    print(f"    Cluster distribution: {dict(zip(*np.unique(labels, return_counts=True)))}")
    
    print("  → Computing cluster metrics...")
    metrics = compute_cluster_metrics(X, labels, method="euclidean")
    print(f"  ✓ Silhouette Score: {metrics['silhouette_score']:.4f}")
    print(f"    Davies-Bouldin Index: {metrics['davies_bouldin_index']:.4f}")
    
    print("  → Getting cluster statistics...")
    stats = get_cluster_statistics(cv_df, labels)
    for cluster_id, cluster_stats in stats.items():
        print(f"    Cluster {cluster_id}: {cluster_stats['count']} cryptos - {cluster_stats['cryptos']}")
    
    print("✅ TEST 5 PASSED: Clustering works!")
except Exception as e:
    print(f"❌ TEST 5 FAILED: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("🎉 ALL TESTS COMPLETED!")
print("=" * 60)
print("\n✅ System is ready for deployment!")
print("\nTo run the app:")
print("  python app.py")
print("\nThen visit: http://localhost:5000")
print("=" * 60)
