from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_rf(X, y):
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=5,
        random_state=42,
        class_weight="balanced"
    )
    model.fit(X, y)
    return model

def predict_next_n_days_prices(model, X, df, n=5):
    preds, probs = [], []
    X_last = X.iloc[-1:].copy()

    for _ in range(n):
        p = model.predict(X_last)[0]
        prob = model.predict_proba(X_last)[0][1]

        preds.append(int(p))
        probs.append(round(prob, 4))

        X_last["return_lag2"] = X_last["return_lag1"]
        X_last["return_lag1"] = 0
        X_last["cv_lag2"] = X_last["cv_lag1"]

    last_price = df["Close"].iloc[-1]
    returns = df["log_return"].dropna()

    avg_daily_return = returns.mean()
    daily_volatility = returns.std()

    predicted_prices = []
    current_price = last_price

    for i in range(n):
        expected_return = (
            avg_daily_return * probs[i]
            if preds[i] == 1
            else -avg_daily_return * (1 - probs[i])
        )

        expected_return += np.random.normal(0, daily_volatility * 0.5)
        current_price *= (1 + expected_return)
        predicted_prices.append(round(current_price, 2))

    return predicted_prices, preds, probs
