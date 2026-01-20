# feature_engineering.py
import numpy as np


def create_target(df):
    df = df.copy()
    log_return = df["log_return"].squeeze()
    df["target"] = (log_return.shift(-1) > 0).astype(int)
    return df


def add_lag_features(df, lags=2):
    df = df.copy()

    for lag in range(1, lags + 1):
        df[f"return_lag{lag}"] = df["log_return"].squeeze().shift(lag)
        df[f"cv_lag{lag}"] = df["cv"].squeeze().shift(lag)

    return df


def build_features(df):
    df = df.copy()

    # target
    df = create_target(df)

    # lag features
    df = add_lag_features(df, lags=2)

    # drop NaN
    df = df.dropna()

    feature_cols = [
        "return_lag1",
        "return_lag2",
        "cv_lag1",
        "cv_lag2",
        "rsi_14",
        "rsi_slope"
    ]

    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing features: {missing}")
    
    X = df[feature_cols]
    y = df["target"]

    return X, y
