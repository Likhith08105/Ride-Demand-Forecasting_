from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

from app.services.predictor import predict_demand
from app.services.clustering import get_zone_type

import random

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="app/templates")

# In-memory prediction history
prediction_history = []
MAX_HISTORY = 10

# Weather encoding map
WEATHER_MAP = {
    "Clear": 0,
    "Cloudy": 1,
    "Rainy": 2,
    "Fog": 1,
    "Snow": 2
}

class PredictionRequest(BaseModel):
    year: int
    month: int
    day_of_week: int
    hour: int
    temperature: float
    humidity: float
    wind_speed: float
    weather_condition: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        weather_encoded = WEATHER_MAP.get(data.weather_condition, 0)

        features = {
            "year": data.year,
            "month": data.month,
            "day_of_week": data.day_of_week,
            "hour": data.hour,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "wind_speed": data.wind_speed,
            "weather_encoded": weather_encoded,
            "latitude": 17.45,
            "longitude": 78.48,
            "distance_km": random.uniform(3, 12)
        }

        # ML Prediction
        prediction = round(predict_demand(features), 2)

        # Zone logic
        zone = get_zone_type(
            features["latitude"],
            features["longitude"],
            prediction
        )

        # Analysis text
        prediction_analysis = (
            f"The predicted demand is influenced by time, weather conditions, "
            f"and day pattern. This area currently falls under a {zone.lower()}, "
            f"indicating moderate to high ride activity."
        )

        # Input summary
        input_summary = {
            "Year": data.year,
            "Month": data.month,
            "Day of Week": data.day_of_week,
            "Hour": data.hour,
            "Temperature (°C)": data.temperature,
            "Humidity (%)": data.humidity,
            "Wind Speed (km/h)": data.wind_speed,
            "Weather Condition": data.weather_condition
        }

        # Chart data
        hour_labels = list(range(24))
        hour_values = [
            max(5, prediction + random.randint(-8, 8))
            for _ in range(24)
        ]

        # Save to history (in-memory)
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": prediction,
            "zone": zone,
            "inputs": input_summary
        }
        prediction_history.insert(0, history_entry)
        if len(prediction_history) > MAX_HISTORY:
            prediction_history.pop()

        return {
            "success": True,
            "prediction": prediction,
            "zone": zone,
            "analysis": prediction_analysis,
            "input_summary": input_summary,
            "hour_labels": hour_labels,
            "hour_values": hour_values
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/history")
def get_history():
    return {
        "success": True,
        "history": prediction_history
    }
