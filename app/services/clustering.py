import joblib
import numpy as np

# Load clustering model and scaler
kmeans = joblib.load("model/kmeans_model.pkl")
scaler = joblib.load("model/cluster_scaler.pkl")

def get_zone_type(latitude: float, longitude: float, demand: float) -> str:
    """
    Identify demand zone using K-Means clustering
    """

    features = np.array([[latitude, longitude, demand]])
    scaled_features = scaler.transform(features)

    cluster = kmeans.predict(scaled_features)[0]

    if cluster == 2:
        return "High Demand Zone"
    elif cluster == 1:
        return "Medium Demand Zone"
    else:
        return "Low Demand Zone"
