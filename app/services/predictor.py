import joblib
import numpy as np

# Load trained XGBoost model
model = joblib.load("model/demand_model.pkl")

def predict_demand(features: dict) -> float:
    """
    Predict ride demand using trained XGBoost model
    """

    feature_array = np.array([[
        features["year"],
        features["month"],
        features["day_of_week"],
        features["hour"],
        features["temperature"],
        features["humidity"],
        features["wind_speed"],
        features["weather_encoded"],
        features["latitude"],
        features["longitude"],
        features["distance_km"]
    ]])

    prediction = model.predict(feature_array)[0]

    return round(float(prediction), 2)
