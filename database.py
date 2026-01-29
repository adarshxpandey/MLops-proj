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

def get_analytics_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Total predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    # 2. Top locations
    cursor.execute("""
        SELECT location, COUNT(*) as cnt
        FROM predictions
        GROUP BY location
        ORDER BY cnt DESC
        LIMIT 5
    """)
    top_locations = [
        {"location": row[0], "count": row[1]}
        for row in cursor.fetchall()
    ]

    # 3. Average price by BHK
    cursor.execute("""
        SELECT bhk, ROUND(AVG(predicted_price), 2)
        FROM predictions
        GROUP BY bhk
        ORDER BY bhk
    """)
    avg_price_by_bhk = [
        {"bhk": row[0], "avg_price": row[1]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "total_predictions": total_predictions,
        "top_locations": top_locations,
        "avg_price_by_bhk": avg_price_by_bhk
    }
