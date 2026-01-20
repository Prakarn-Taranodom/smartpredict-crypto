import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from tslearn.clustering import TimeSeriesKMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, davies_bouldin_score
from tslearn.metrics import cdist_dtw
import warnings
warnings.filterwarnings("ignore")


# =================================================
# EUCLIDEAN KMEANS
# =================================================
class EuclideanKMeansClustering:
    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.labels_ = None
        self.inertia_ = None

    def fit_predict(self, X):
        model = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10
        )
        self.labels_ = model.fit_predict(X)
        self.inertia_ = float(model.inertia_)
        return self.labels_

    def get_cluster_assignments(self, stock_ids):
        return pd.DataFrame({
            "stock_id": stock_ids,
            "cluster": self.labels_
        })


# =================================================
# DTW KMEANS (ปรับให้เร็วขึ้น)
# =================================================
class DTWKMeansClustering:
    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.labels_ = None
        self.inertia_ = None

    def fit_predict(self, X):
        X_reshaped = X.reshape(X.shape[0], X.shape[1], 1)

        model = TimeSeriesKMeans(
            n_clusters=self.n_clusters,
            metric="dtw",
            random_state=self.random_state,
            n_init=3,  # ลดจาก 5 เป็น 3
            max_iter=50  # จำกัด iterations
        )

        self.labels_ = model.fit_predict(X_reshaped)

        self.inertia_ = (
            float(model.inertia_)
            if hasattr(model, "inertia_") and model.inertia_ is not None
            else float(np.sum(model._distances))
        )

        return self.labels_

    def get_cluster_assignments(self, stock_ids):
        return pd.DataFrame({
            "stock_id": stock_ids,
            "cluster": self.labels_
        })


# =================================================
# ELBOW
# =================================================
def compute_elbow_curve(X, k_range, method="dtw"):
    inertia = []

    for k in k_range:
        if method == "dtw":
            model = DTWKMeansClustering(k)
        else:
            model = EuclideanKMeansClustering(k)

        model.fit_predict(X)
        inertia.append(float(model.inertia_))

    return {
        "k_values": list(k_range),
        "inertia_values": inertia
    }


def detect_elbow_point(inertia, k_values):
    inertia = np.array(inertia, dtype=float)
    k_values = np.array(k_values)

    if len(inertia) < 3:
        return {
            "elbow_k": int(k_values[0]),
            "elbow_index": 0,
            "method": "fallback",
            "reasoning": "Not enough data points for elbow detection"
        }

    # Normalize data to [0, 1]
    k_norm = (k_values - k_values.min()) / (k_values.max() - k_values.min())
    inertia_norm = (inertia - inertia.min()) / (inertia.max() - inertia.min())
    
    # Calculate distance from each point to the line connecting first and last points
    # Line: from (k_norm[0], inertia_norm[0]) to (k_norm[-1], inertia_norm[-1])
    x1, y1 = k_norm[0], inertia_norm[0]
    x2, y2 = k_norm[-1], inertia_norm[-1]
    
    distances = []
    for i in range(len(k_norm)):
        x0, y0 = k_norm[i], inertia_norm[i]
        # Distance from point to line formula
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distance = numerator / denominator if denominator > 0 else 0
        distances.append(distance)
    
    # Elbow is the point with maximum distance
    elbow_index = int(np.argmax(distances))
    elbow_k = int(k_values[elbow_index])
    elbow_y = float(inertia[elbow_index])
    
    # Calculate improvement metrics
    if elbow_index > 0 and elbow_index < len(inertia) - 1:
        improvement_before = inertia[elbow_index-1] - inertia[elbow_index]
        improvement_after = inertia[elbow_index] - inertia[elbow_index+1]
        reasoning = f"K={elbow_k} selected as elbow point with maximum distance from baseline. Inertia improvement: before={improvement_before:.2f}, after={improvement_after:.2f}"
    else:
        reasoning = f"K={elbow_k} selected as elbow point with maximum distance from baseline"
    
    return {
        "elbow_k": elbow_k,
        "elbow_index": elbow_index,
        "elbow_y_value": elbow_y,
        "method": "kneedle",
        "reasoning": reasoning
    }


# =================================================
# VISUALIZATION (PCA / TSNE)
# =================================================
def compute_cluster_visualization_data(X, labels, method="pca"):
    if method == "pca":
        reducer = PCA(n_components=2, random_state=42)
    else:
        reducer = TSNE(
            n_components=2,
            random_state=42,
            perplexity=min(30, len(X) - 1)
        )

    X2 = reducer.fit_transform(X)

    return {
        "x": X2[:, 0].tolist(),
        "y": X2[:, 1].tolist(),
        "labels": labels.tolist()
    }


# =================================================
# CLUSTER EVALUATION METRICS
# =================================================
def compute_cluster_metrics(X, labels, method="euclidean"):
    """
    คำนวณ Silhouette Score และ Davies-Bouldin Index
    """
    try:
        if method == "dtw":
            # DTW distance matrix
            X_reshaped = X.reshape(X.shape[0], X.shape[1], 1)
            dist_matrix = cdist_dtw(X_reshaped, X_reshaped)
            silhouette = silhouette_score(dist_matrix, labels, metric='precomputed')
        else:
            # Euclidean distance
            silhouette = silhouette_score(X, labels, metric='euclidean')
        
        # Davies-Bouldin (ใช้ Euclidean เสมอ)
        davies_bouldin = davies_bouldin_score(X, labels)
        
        return {
            "silhouette_score": float(silhouette),
            "davies_bouldin_index": float(davies_bouldin)
        }
    except Exception as e:
        return {
            "silhouette_score": None,
            "davies_bouldin_index": None,
            "error": str(e)
        }


# =================================================
# CLUSTER STATS
# =================================================
def get_cluster_statistics(df, labels):
    stats = {}

    for c in np.unique(labels):
        mask = labels == c
        stats[int(c)] = {
            "count": int(mask.sum()),
            "stocks": df.loc[mask, "stock_id"].tolist()
        }

    return stats
