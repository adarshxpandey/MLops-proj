from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sqlite3

from model import predict_price, MODEL_VERSION, VALID_LOCATIONS, get_weather_data
from database import init_db, save_prediction, get_all_predictions


app = FastAPI(title="Bangalore House Price Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/ui", StaticFiles(directory="static", html=True), name="ui")
init_db()


class PredictionRequest(BaseModel):
    area_sqft: float
    bhk: int
    bath: int
    location: str


@app.get("/")
def root():
    """Render health check + browser root route."""
    return FileResponse("static/index.html")


@app.post("/predict")
def predict(request: PredictionRequest):
    if request.location not in VALID_LOCATIONS:
        return {
            "success": False,
            "error": "Invalid location"
        }

    try:
        prediction = predict_price(
            area_sqft=request.area_sqft,
            bath=request.bath,
            bhk=request.bhk,
            location=request.location
        )

        weather_data = get_weather_data(request.location)

        save_prediction(
            area_sqft=request.area_sqft,
            bhk=request.bhk,
            bath=request.bath,
            location=request.location,
            predicted_price=prediction,
            temperature=weather_data["temperature"],
            is_raining=weather_data["is_raining"],
            metro_distance=weather_data["metro_distance"],
            model_version=MODEL_VERSION
        )

        return {
            "success": True,
            "area_sqft": request.area_sqft,
            "bhk": request.bhk,
            "bath": request.bath,
            "location": request.location,
            "predicted_price_lakhs": float(prediction),
            "weather": weather_data,
            "model_version": MODEL_VERSION
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/predictions")
def read_predictions():
    rows = get_all_predictions()
    return [
        {
            "area_sqft": r["area_sqft"],
            "bhk": r["bhk"],
            "bath": r["bath"],
            "location": r["location"],
            "predicted_price": round(r["predicted_price"], 2),
            "model_version": r["model_version"],
            "timestamp": r["timestamp"]
        }
        for r in rows
    ]


@app.get("/locations")
def get_locations():
    return VALID_LOCATIONS


@app.get("/analytics/summary")
def get_analytics_summary():
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    total = cursor.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]

    top_locations = cursor.execute("""
        SELECT location, COUNT(*) as count
        FROM predictions
        GROUP BY location
        ORDER BY count DESC
        LIMIT 5
    """).fetchall()

    avg_by_bhk = cursor.execute("""
        SELECT bhk, AVG(predicted_price) as avg_price
        FROM predictions
        GROUP BY bhk
    """).fetchall()

    conn.close()

    return {
        "total_predictions": total,
        "top_locations": [
            {"location": r[0], "count": r[1]} for r in top_locations
        ],
        "avg_price_by_bhk": [
            {"bhk": r[0], "avg_price": round(r[1], 2)} for r in avg_by_bhk
        ]
    }


@app.get("/predictions/recent")
def recent_predictions(limit: int = 10):
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT area_sqft, bhk, bath, location, predicted_price, timestamp
        FROM predictions
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "area_sqft": r[0],
            "bhk": r[1],
            "bath": r[2],
            "location": r[3],
            "predicted_price": r[4],
            "timestamp": r[5]
        }
        for r in rows
    ]