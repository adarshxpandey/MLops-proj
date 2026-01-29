import joblib
import numpy as np
import pandas as pd
import requests
from math import radians, cos, sin, asin, sqrt

MODEL_VERSION = "bengaluru_rf_v1"

# Load trained model
model_data = joblib.load("bangalore_price_model.pkl")
model = model_data["model"]
columns = model_data["columns"]

# --------------------------------------------------
# Location coordinates (Bangalore metro area)
# --------------------------------------------------
_ALL_LOCATION_COORDS = {
    "Whitefield": (12.9698, 77.7499),
    "Koramangala": (12.9352, 77.6245),
    "Indiranagar": (12.9716, 77.6412),
    "JP Nagar": (12.9352, 77.6068),
    "Marathahalli": (12.9479, 77.6999),
    "HSR Layout": (12.9250, 77.6245),
    "Bellandur": (12.9352, 77.6699),
    "Sarjapur Road": (12.8956, 77.6445),
    "Yeshwantpur": (13.0016, 77.5729),
    "Nagavara": (13.0299, 77.5891),
    "Ulsoor": (12.9847, 77.5973),
    "Cubbon Park": (12.9674, 77.5895),
    "Vidhana Soudha": (12.9682, 77.5903),
    "Majestic": (12.9656, 77.5745),
}

# Only keep locations that have coordinates defined
VALID_LOCATIONS = sorted(
    col.replace("location_", "")
    for col in columns
    if col.startswith("location_") and col.replace("location_", "") in _ALL_LOCATION_COORDS
)

LOCATION_COORDS = {loc: _ALL_LOCATION_COORDS[loc] for loc in VALID_LOCATIONS}

# Bangalore Metro stations (Line 1 & 2) - lat, lon
METRO_STATIONS = [
    (13.0299, 77.5891),  # Nagavara
    (12.9847, 77.5973),  # Ulsoor
    (12.9674, 77.5895),  # Cubbon Park
    (12.9682, 77.5903),  # Vidhana Soudha
    (12.9656, 77.5745),  # Majestic
    (12.9479, 77.6999),  # Marathahalli
    (12.9698, 77.7499),  # Whitefield
    (12.8956, 77.6445),  # Sarjapur Road
]

OPENWEATHER_API_KEY = "4b0b6d380c58fb0166f7fe06f076888b"  # REPLACE WITH YOUR KEY


def haversine(lon1, lat1, lon2, lat2):
    """Calculate distance between two points in km."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def get_weather_data(location):
    """Fetch real weather from OpenWeatherMap API."""
    try:
        # Get location coordinates
        coords = LOCATION_COORDS.get(location, (12.9716, 77.5946))
        lat, lon = coords
        
        # Fetch weather
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        temperature = data["main"]["temp"]
        is_raining = 1 if "rain" in data else 0
        
        # Calculate metro distance
        min_distance = min(
            haversine(lon, lat, metro_lon, metro_lat)
            for metro_lat, metro_lon in METRO_STATIONS
        )
        metro_distance = round(min_distance, 2)
        
        return {
            "temperature": round(temperature, 1),
            "is_raining": is_raining,
            "metro_distance": metro_distance
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return get_default_weather_data()


def get_default_weather_data():
    """Fallback defaults if API fails."""
    return {
        "temperature": 26.0,
        "is_raining": 0,
        "metro_distance": 2.5
    }


def predict_price(area_sqft, bath, bhk, location):
    if location not in VALID_LOCATIONS:
        raise ValueError("Invalid location")

    input_dict = {
        "total_sqft": area_sqft,
        "bath": bath,
        "bhk": bhk
    }

    for col in columns:
        if col.startswith("location_"):
            input_dict[col] = 1 if col == f"location_{location}" else 0

    df = pd.DataFrame([input_dict])
    df = df.reindex(columns=columns, fill_value=0)

    prediction = model.predict(df)[0]
    return round(prediction, 2)
    prediction = model.predict(df)[0]
    return round(prediction, 2)
    return round(prediction, 2)
MODEL_METADATA = {
    "version": "v1.0.0",
    "trained_on": "Bengaluru House Prices (Kaggle)",
    "records": 13320,
    "algorithm": "Linear Regression",
    "last_trained": "2026-01-20"
}
