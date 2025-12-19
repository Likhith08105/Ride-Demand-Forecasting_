from pydantic import BaseModel

class PredictionInput(BaseModel):
    year: int
    month: int
    day_of_week: int
    hour: int
    temperature: float
    humidity: float
    wind_speed: float
    weather_encoded: int
    latitude: float
    longitude: float
    distance_km: float


class PredictionResponse(BaseModel):
    predicted_demand: float
    zone_type: str
