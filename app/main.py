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


from pydantic import BaseModel, Field, validator
from typing import Literal

class PredictionRequest(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    hour: int = Field(..., ge=0, le=23, description="Hour (0-23)")
    temperature: float = Field(..., ge=-50, le=60, description="Temperature in Celsius")
    day_type: Literal["Weekday", "Weekend", "Holiday"]
    weather_condition: str
    location_zone: str

    @validator("weather_condition")
    def validate_weather(cls, v):
        allowed = {"Clear", "Cloudy", "Rainy", "Fog", "Snow"}
        if v not in allowed:
            raise ValueError(f"weather_condition must be one of {allowed}")
        return v

    @validator("location_zone")
    def validate_zone(cls, v):
        allowed = {"Central", "Suburb", "IT Park", "Airport", "Mall", "University", "Hospital", "Stadium", "Industrial", "Residential"}
        if v not in allowed:
            raise ValueError(f"location_zone must be one of {allowed}")
        return v

class PredictionResponse(BaseModel):
    predicted_demand: float
    location_zone: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


from fastapi import Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest = Body(...)):
    try:
        weather_encoded = WEATHER_MAP.get(data.weather_condition, 0)

        # Lag features: use previous predictions if available, else mean value
        lag_1 = prediction_history[0]["prediction"] if prediction_history else 30.0
        lag_24 = prediction_history[23]["prediction"] if len(prediction_history) > 23 else 30.0


        # Location zone mapping (must match training)
        zone_map = {
            "Central": 0,
            "Suburb": 1,
            "IT Park": 2,
            "Airport": 3,
            "Mall": 4,
            "University": 5,
            "Hospital": 6,
            "Stadium": 7,
            "Industrial": 8,
            "Residential": 9
        }
        zone_encoded = zone_map.get(data.location_zone, 0)

        features = {
            "month": data.month,
            "hour": data.hour,
            "day_type": 0 if data.day_type == "Weekday" else 1,
            "weather_condition": weather_encoded,
            "temperature": data.temperature,
            "location_zone": zone_encoded,
            "lag_1": lag_1,
            "lag_24": lag_24
        }

        # ML Prediction

        prediction = round(predict_demand(features), 2)

        # Save to history (in-memory)
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": prediction,
            "zone": data.location_zone,
            "inputs": {
                "Month": data.month,
                "Hour": data.hour,
                "Day Type": data.day_type,
                "Temperature (°C)": data.temperature,
                "Weather Condition": data.weather_condition,
                "Location Zone": data.location_zone
            }
        }
        prediction_history.insert(0, history_entry)
        if len(prediction_history) > MAX_HISTORY:
            prediction_history.pop()

        response = PredictionResponse(predicted_demand=prediction, location_zone=data.location_zone)
        return JSONResponse(content=jsonable_encoder(response))

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
