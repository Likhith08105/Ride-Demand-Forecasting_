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



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


from fastapi import Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

@app.post("/predict")
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


        # Dynamic, context-aware analysis
        analysis_parts = []
        # IT Park
        if data.location_zone == "IT Park":
            if data.day_type == "Weekend":
                analysis_parts.append("Leisure and late-evening trips increase demand variability in IT Park on weekends.")
            else:
                analysis_parts.append("Office commute significantly drives demand peaks in IT Park on weekdays.")
        # Airport
        elif data.location_zone == "Airport":
            if data.hour in range(5, 11):
                analysis_parts.append("Morning flight schedules boost early demand at the Airport.")
            elif data.hour in range(18, 23):
                analysis_parts.append("Evening arrivals and departures create high demand at the Airport.")
            else:
                analysis_parts.append("Airport demand is steady due to continuous flight operations.")
        # Central
        elif data.location_zone == "Central":
            if data.hour in range(8, 21):
                analysis_parts.append("Central zone sees high activity during business and shopping hours.")
            else:
                analysis_parts.append("Late-night demand in Central is driven by nightlife and events.")
        # Rainy weather
        if data.weather_condition == "Rainy":
            analysis_parts.append("Rainy weather typically increases ride demand as people avoid walking or biking.")
        # Rush hour
        if data.hour in range(8, 11) or data.hour in range(17, 21):
            analysis_parts.append("This is a rush hour period, so demand is expected to spike.")
        # Suburb on weekend
        if data.location_zone == "Suburb" and data.day_type == "Weekend":
            analysis_parts.append("Suburban leisure trips and family outings can increase weekend demand.")
        # Mall on weekend
        if data.location_zone == "Mall" and data.day_type == "Weekend":
            analysis_parts.append("Weekend shopping and entertainment drive up demand near malls.")
        # Default if nothing else
        if not analysis_parts:
            analysis_parts.append("Demand is shaped by the interplay of time, weather, and zone activity.")
        prediction_analysis = " ".join(analysis_parts) + f" This area ({data.location_zone}) currently shows demand of {prediction}."

        # Input summary
        input_summary = {
            "Month": data.month,
            "Hour": data.hour,
            "Day Type": data.day_type,
            "Temperature (°C)": data.temperature,
            "Weather Condition": data.weather_condition,
            "Location Zone": data.location_zone
        }

        # Chart data
        hour_labels = list(range(24))
        hour_values = [max(5, prediction + random.randint(-8, 8)) for _ in range(24)]

        # Save to history (in-memory)
        history_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": prediction,
            "zone": data.location_zone,
            "inputs": input_summary
        }
        prediction_history.insert(0, history_entry)
        if len(prediction_history) > MAX_HISTORY:
            prediction_history.pop()

        return {
            "success": True,
            "prediction": prediction,
            "zone": data.location_zone,
            "analysis": prediction_analysis,
            "input_summary": input_summary,
            "hour_labels": hour_labels,
            "hour_values": hour_values
        }

    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        }, status_code=400)

@app.get("/history")
def get_history():
    return {
        "success": True,
        "history": prediction_history
    }
