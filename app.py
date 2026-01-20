from flask import Flask, render_template, request, redirect, url_for, jsonify
from fetch_crypto import fetch_crypto_data as fetch_stock_data
from volatility_pipeline import compute_conditional_volatility
from feature_engineering import build_features
from train_model import predict_next_n_days_prices, train_rf
from data_preparation_crypto import prepare_market_data
from clustering_module import (
    DTWKMeansClustering,
    EuclideanKMeansClustering,
    compute_elbow_curve,
    compute_cluster_visualization_data,
    get_cluster_statistics,
    detect_elbow_point,
    compute_cluster_metrics
)

import pandas as pd
import numpy as np

app = Flask(__name__)

# =================================================
# INDEX
# =================================================
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# =================================================
# PREDICT (ไม่แตะ)
# =================================================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    result = None
    ticker = None

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper()

        if not ticker:
            return render_template("predict.html", error="Please enter a crypto symbol")

        try:
            df = fetch_stock_data(ticker)
            df_cv = compute_conditional_volatility(df)
            X, y = build_features(df_cv)

            model = train_rf(X, y)
            predicted_prices, preds, probs = predict_next_n_days_prices(
                model, X, df_cv, n=5
            )

            last_date = pd.to_datetime(df_cv.index[-1])
            future_dates = [
                (last_date + pd.Timedelta(days=i + 1)).strftime("%Y-%m-%d")
                for i in range(5)
            ]

            dates = pd.to_datetime(df_cv.index).strftime("%Y-%m-%d").tolist()
            prices = df_cv["Close"].round(2).tolist()
            cv_values = df_cv["cv"].round(4).tolist()
            importance = (
                pd.Series(model.feature_importances_, index=X.columns)
                .sort_values(ascending=False)
            )

            result = {
                "ticker": ticker,
                "predictions": [
                    {
                        "date": d,
                        "prediction": "UP" if p == 1 else "DOWN",
                        "probability": round(float(prob), 4),
                        "predicted_price": round(float(price), 2),
                    }
                    for d, p, prob, price in zip(
                        future_dates, preds, probs, predicted_prices
                    )
                ],
                "dates": dates,
                "prices": prices,
                "cv": cv_values,
                "feat_items": list(
                    zip(
                        importance.index.tolist(),
                        importance.values.round(4).tolist(),
                    )
                ),
            }

        except Exception as e:
            return render_template("predict.html", error=str(e), ticker=ticker)

    return render_template("predict.html", result=result, ticker=ticker)


# =================================================
# CLUSTER ENTRY
# =================================================
@app.route("/cluster", methods=["GET", "POST"])
def cluster():
    return render_template("cluster.html")


# =================================================
# ✅ API: STOCK LIST (แก้ Unexpected token '<')
# =================================================
@app.route("/api/cryptos/<market>")
def api_cryptos(market):
    try:
        cv_df = prepare_market_data(
            market,
            window_days=60,
            include_category=True
        )

        cryptos_by_category = {}

        for _, row in cv_df.iterrows():
            category = row.get("category", "Unknown")
            crypto_id = row.get("crypto_id")

            cryptos_by_category.setdefault(category, []).append({
                "symbol": crypto_id,
                "name": crypto_id
            })

        return jsonify({
            "cryptos_by_category": cryptos_by_category,
            "total_cryptos": len(cv_df)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================================================
# CLUSTER: Step 1 - Select Method
# =================================================
@app.route("/cluster/select-method/<market>")
def cluster_select_method(market):
    return render_template("cluster_select_method.html", market=market)


# =================================================
# CLUSTER: Step 2 - Show Elbow Plot (รับ stocks)
# =================================================
@app.route("/cluster/elbow/<market>")
def cluster_elbow(market):
    method = request.args.get("method", "dtw")
    stocks_param = request.args.get("stocks", "")
    
    try:
        if stocks_param:
            selected_cryptos = stocks_param.split(',')
            from data_preparation_crypto import prepare_crypto_data_for_clustering
            cv_df = prepare_crypto_data_for_clustering(
                selected_cryptos,
                window_days=60,
                include_category=True
            )
        else:
            cv_df = prepare_market_data(
                market,
                window_days=60,
                include_category=True
            )

        if len(cv_df) < 3:
            return render_template(
                "cluster_elbow.html",
                elbow_data={"error": "Not enough cryptos"},
                market=market
            )

        X = cv_df.iloc[:, 1:-1].values

        elbow_data = compute_elbow_curve(
            X,
            k_range=range(2, min(10, len(X))),
            method=method
        )

        elbow_info = detect_elbow_point(
            elbow_data["inertia_values"],
            elbow_data["k_values"]
        )

        elbow_data.update(elbow_info)
        elbow_data["method"] = method
        elbow_data["stocks"] = stocks_param  # เก็บ stocks ไว้ส่งต่อ

        return render_template(
            "cluster_elbow.html",
            elbow_data=elbow_data,
            market=market
        )

    except Exception as e:
        return render_template(
            "cluster_elbow.html",
            elbow_data={"error": str(e)},
            market=market
        )


# =================================================
# CLUSTER RESULT (รับ stocks parameter)
# =================================================
@app.route("/cluster/result/<market>/<int:k>")
def cluster_result(market, k):
    method = request.args.get("method", "dtw")
    stocks_param = request.args.get("stocks", "")

    try:
        if stocks_param:
            selected_cryptos = stocks_param.split(',')
            from data_preparation_crypto import prepare_crypto_data_for_clustering
            cv_df = prepare_crypto_data_for_clustering(
                selected_cryptos,
                window_days=60,
                include_category=True
            )
        else:
            cv_df = prepare_market_data(
                market,
                window_days=60,
                include_category=True
            )

        if len(cv_df) < 3:
            return render_template(
                "cluster_result.html",
                result={"error": "Not enough cryptos for clustering"},
                market=market,
                category_filter="all"
            )

        X = cv_df.iloc[:, 1:-1].values
        crypto_ids = cv_df["crypto_id"].values

        clustering = (
            DTWKMeansClustering(k)
            if method == "dtw"
            else EuclideanKMeansClustering(k)
        )

        labels = clustering.fit_predict(X)
        metrics = compute_cluster_metrics(X, labels, method=method)

        assignments_df = clustering.get_cluster_assignments(crypto_ids)
        assignments_df["category"] = cv_df["category"].values

        viz_pca = compute_cluster_visualization_data(X, labels, method="pca")
        cluster_stats = get_cluster_statistics(cv_df, labels)

        result = {
            "market": market,
            "method": method,
            "optimal_k": k,
            "metrics": metrics,
            "assignments": assignments_df.to_dict("records"),
            "cluster_stats": cluster_stats,
            "viz_pca": viz_pca
        }

        return render_template(
            "cluster_result.html",
            result=result,
            market=market,
            category_filter="all"
        )

    except Exception as e:
        return render_template(
            "cluster_result.html",
            result={"error": str(e)},
            market=market,
            category_filter="all"
        )


# =================================================
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
