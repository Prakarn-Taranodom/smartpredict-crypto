print("TEST_RF STARTED")

from fetch_stock import fetch_stock_data
from volatility_pipeline import compute_conditional_volatility
from feature_engineering import build_features
from train_model import train_rf, predict_next_day
import pandas as pd
def main():
    print("INSIDE MAIN")
    ticker = "AAPL"

    print("Fetching data...")
    df = fetch_stock_data(ticker)

    print("Computing CV...")
    df_cv = compute_conditional_volatility(df)

    print("Building features...")
    X, y = build_features(df_cv)

    print("Training Random Forest...")
    model = train_rf(X, y)

    print("Predicting...")
    pred, prob = predict_next_day(model, X)

    print("\nRESULT")
    print("Ticker:", ticker)
    print("Prediction (1=UP, 0=DOWN):", pred)
    print("Probability UP:", round(prob, 4))
    importance = pd.Series(
    model.feature_importances_,
    index=X.columns).sort_values(ascending=False)

    print("\nFeature Importance:")
    print(importance)
    




if __name__ == "__main__":
    main()
