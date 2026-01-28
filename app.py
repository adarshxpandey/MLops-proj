from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

from model import predict_price, MODEL_VERSION, VALID_LOCATIONS, get_weather_data
from database import init_db, save_prediction, get_all_predictions







from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bangalore House Price Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)







# --------------------------------------------------
# App setup
# --------------------------------------------------
app = FastAPI(title="Bangalore House Price Predictor")
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

init_db()


# --------------------------------------------------
# Request schema
# --------------------------------------------------
class PredictionRequest(BaseModel):
    area_sqft: float
    bhk: int
    bath: int
    location: str


# --------------------------------------------------
# Predict endpoint
# --------------------------------------------------
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


# --------------------------------------------------
# History endpoint
# --------------------------------------------------
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


# --------------------------------------------------
# Locations endpoint (SOURCE OF TRUTH)
# --------------------------------------------------
@app.get("/locations")
def get_locations():
    return VALID_LOCATIONS
