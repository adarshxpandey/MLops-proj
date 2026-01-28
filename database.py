import sqlite3
from datetime import datetime

DB_NAME = "predictions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_sqft REAL,
            bhk INTEGER,
            bath INTEGER,
            location TEXT,
            predicted_price REAL,
            temperature REAL,
            is_raining INTEGER,
            metro_distance REAL,
            model_version TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(
    area_sqft,
    bhk,
    bath,
    location,
    predicted_price,
    temperature,
    is_raining,
    metro_distance,
    model_version
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            area_sqft, bhk, bath, location,
            predicted_price, temperature, is_raining,
            metro_distance, model_version, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        area_sqft,
        bhk,
        bath,
        location,
        predicted_price,
        temperature,
        is_raining,
        metro_distance,
        model_version,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_all_predictions():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY timestamp DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
