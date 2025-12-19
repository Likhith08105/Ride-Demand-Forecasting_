
import pandas as pd
import numpy as np

np.random.seed(42)

# Number of records
num_records = 6000

# Time features
months = np.random.randint(1, 13, num_records)
hours = np.random.randint(0, 24, num_records)
days_of_week = np.random.randint(0, 7, num_records)   # 0 = Monday
day_type = np.where(days_of_week < 5, "Weekday", "Weekend")

# Weather features
temperature = np.random.uniform(18, 40, num_records)   # °C
weather_conditions = pd.Series(
    np.random.choice(
        ["Clear", "Cloudy", "Rainy"],
        num_records,
        p=[0.55, 0.30, 0.15]
    )
)
weather_encoded = weather_conditions.map({
    "Clear": 0,
    "Cloudy": 1,
    "Rainy": 2
})

# Location Zone (cluster or pickup area)
location_zones = pd.Series(
    np.random.choice(
        ["Central", "Suburb", "IT Park", "Airport", "Mall", "University", "Hospital", "Stadium", "Industrial", "Residential"],
        num_records
    )
)

# Demand simulation logic
base_demand = np.random.randint(5, 15, num_records)
peak_hour_boost = (
    ((hours >= 8) & (hours <= 10)) |
    ((hours >= 17) & (hours <= 20))
) * np.random.randint(15, 30, num_records)
weather_boost = (weather_encoded == 2) * np.random.randint(5, 12, num_records)
zone_boost = location_zones.map({
    "Central": 10,
    "IT Park": 8,
    "Airport": 12,
    "Mall": 7,
    "University": 6,
    "Hospital": 5,
    "Stadium": 4,
    "Industrial": 9,
    "Residential": 3,
    "Suburb": 2
})

ride_demand = base_demand + peak_hour_boost + weather_boost + zone_boost

# Lag features (internal, not in UI)

lag_1 = np.roll(ride_demand, 1).astype(float)
lag_24 = np.roll(ride_demand, 24).astype(float)
lag_1[0] = np.nan
lag_24[:24] = np.nan

# Create DataFrame
df = pd.DataFrame({
    "month": months,
    "hour": hours,
    "day_type": day_type,
    "weather_condition": weather_conditions,
    "temperature": temperature,
    "location_zone": location_zones,
    "ride_demand": ride_demand,
    "lag_1": lag_1,
    "lag_24": lag_24
})

# Save CSV
df.to_csv("data/ride_data.csv", index=False)

print("Production-ready ride dataset generated successfully!")
