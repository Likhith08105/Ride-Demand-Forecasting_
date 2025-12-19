from pydantic import BaseModel


class PredictionInput(BaseModel):
    month: int
    hour: int
    day_type: str  # "Weekday" or "Weekend"
    weather_condition: str  # "Clear", "Cloudy", "Rainy"
    temperature: float
    location_zone: str  # e.g. "Central", "Suburb", etc.



class PredictionResponse(BaseModel):
    predicted_demand: float
    location_zone: str
