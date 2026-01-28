import requests

API_KEY = "4b0b6d380c58fb0166f7fe06f076888b"

def get_weather(city="Bangalore"):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        res = requests.get(url, timeout=5)
        data = res.json()

        temperature = data["main"]["temp"]
        is_raining = any(
            w["main"].lower() == "rain"
            for w in data.get("weather", [])
        )

        return {
            "temperature": temperature,
            "is_raining": int(is_raining)
        }

    except Exception:
        # fail safe – never break prediction
        return {
            "temperature": None,
            "is_raining": None
        }
