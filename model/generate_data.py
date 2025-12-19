import pandas as pd
import numpy as np

np.random.seed(42)

# Number of records
num_records = 6000

# Time features
years = np.random.choice([2023, 2024, 2025], num_records)
months = np.random.randint(1, 13, num_records)
days_of_week = np.random.randint(0, 7, num_records)   # 0 = Monday
hours = np.random.randint(0, 24, num_records)

# Weather features
temperature = np.random.uniform(18, 40, num_records)   # °C
humidity = np.random.uniform(30, 90, num_records)      # %
wind_speed = np.random.uniform(0, 25, num_records)     # km/h

# Weather condition (convert to Pandas Series)
weather_conditions = pd.Series(
    np.random.choice(
        ["Clear", "Cloudy", "Rainy"],
        num_records,
        p=[0.55, 0.30, 0.15]
    )
)

# Encode weather condition
weather_encoded = weather_conditions.map({
    "Clear": 0,
    "Cloudy": 1,
    "Rainy": 2
})

# Location features
latitudes = np.random.uniform(17.3, 17.6, num_records)
longitudes = np.random.uniform(78.3, 78.6, num_records)

# Distance in km
distance_km = np.random.uniform(1, 30, num_records)

# Demand simulation logic
base_demand = np.random.randint(5, 15, num_records)

peak_hour_boost = (
    ((hours >= 8) & (hours <= 10)) |
    ((hours >= 17) & (hours <= 20))
) * np.random.randint(15, 30, num_records)

weather_boost = (weather_encoded == 2) * np.random.randint(5, 12, num_records)

ride_demand = base_demand + peak_hour_boost + weather_boost

# Create DataFrame
df = pd.DataFrame({
    "year": years,
    "month": months,
    "day_of_week": days_of_week,
    "hour": hours,
    "temperature": temperature,
    "humidity": humidity,
    "wind_speed": wind_speed,
    "weather_condition": weather_conditions,
    "weather_encoded": weather_encoded,
    "latitude": latitudes,
    "longitude": longitudes,
    "distance_km": distance_km,
    "ride_demand": ride_demand
})

# Save CSV
df.to_csv("data/ride_data.csv", index=False)

print("UI-aligned ride dataset generated successfully!")
