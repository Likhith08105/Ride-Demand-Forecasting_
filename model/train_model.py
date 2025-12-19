import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

# Load dataset
data = pd.read_csv("data/ride_data.csv")

# Features used for prediction
feature_cols = [
    "year",
    "month",
    "day_of_week",
    "hour",
    "temperature",
    "humidity",
    "wind_speed",
    "weather_encoded",
    "latitude",
    "longitude",
    "distance_km"
]

X = data[feature_cols]
y = data["ride_demand"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# XGBoost Regression model
model = XGBRegressor(
    n_estimators=250,
    learning_rate=0.08,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# Save trained model
joblib.dump(model, "model/demand_model.pkl")

print("XGBoost demand model trained and saved successfully!")
