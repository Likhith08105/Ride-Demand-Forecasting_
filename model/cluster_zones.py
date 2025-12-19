import pandas as pd
import joblib

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
data = pd.read_csv("data/ride_data.csv")

# Select features for clustering
cluster_features = data[[
    "latitude",
    "longitude",
    "ride_demand"
]]

# Scale features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(cluster_features)

# K-Means clustering
kmeans = KMeans(
    n_clusters=3,   # Low, Medium, High demand zones
    random_state=42
)

data["zone_cluster"] = kmeans.fit_predict(scaled_features)

# Save models
joblib.dump(kmeans, "model/kmeans_model.pkl")
joblib.dump(scaler, "model/cluster_scaler.pkl")

# Save clustered data
data.to_csv("data/ride_data_with_zones.csv", index=False)

print("K-Means clustering completed and models saved!")
