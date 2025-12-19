import joblib
import numpy as np

# Load trained XGBoost model
model = joblib.load("model/demand_model.pkl")


def predict_demand(features: dict) -> float:
    """
    Predict ride demand using trained XGBoost model
    """
    feature_array = np.array([[
        features["month"],
        features["hour"],
        features["day_type"],
        features["weather_condition"],
        features["temperature"],
        # location_zone: encode as int if needed
        int(features["location_zone"]) if not isinstance(features["location_zone"], int) else features["location_zone"],
        features["lag_1"],
        features["lag_24"]
    ]])
    prediction = model.predict(feature_array)[0]
    return round(float(prediction), 2)
