import requests
from config import API_KEY

def get_weather(city):
    if not API_KEY:
        return {
            "success": False,
            "error": "OpenWeather API key is not configured. Add open_weather_api_key to your .env file.",
        }

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json(),
            "status_code": response.status_code,
        }
    except requests.exceptions.HTTPError as exc:
        try:
            payload = response.json()
            message = payload.get("message", str(exc)) if isinstance(payload, dict) else str(exc)
        except ValueError:
            message = str(exc)
        return {
            "success": False,
            "error": message,
            "status_code": response.status_code,
        }
    except requests.exceptions.RequestException as exc:
        return {
            "success": False,
            "error": str(exc),
            "status_code": getattr(exc.response, "status_code", None),
        }