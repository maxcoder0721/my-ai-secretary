"""Weather module — uses Open-Meteo (free, no API key required)."""
from __future__ import annotations

import os
from datetime import datetime
from typing import Any

import requests


WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def get_weather() -> dict[str, Any]:
    """Return today's weather summary for the user's city."""
    lat = os.getenv("USER_LATITUDE", "48.8566")
    lon = os.getenv("USER_LONGITUDE", "2.3522")
    city = os.getenv("USER_CITY", "Paris")
    tz = os.getenv("USER_TIMEZONE", "Europe/Paris")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code,sunrise,sunset"
        f"&timezone={tz}"
        "&forecast_days=1"
    )

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {"error": f"Could not fetch weather: {e}", "city": city}

    current = data.get("current", {})
    daily = data.get("daily", {})

    code = current.get("weather_code", 0)
    description = WMO_CODES.get(code, "Unknown")

    return {
        "city": city,
        "description": description,
        "current_temp": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_kmh": current.get("wind_speed_10m"),
        "max_temp": (daily.get("temperature_2m_max") or [None])[0],
        "min_temp": (daily.get("temperature_2m_min") or [None])[0],
        "rain_chance": (daily.get("precipitation_probability_max") or [None])[0],
        "sunrise": (daily.get("sunrise") or [None])[0],
        "sunset": (daily.get("sunset") or [None])[0],
    }


def format_weather_html(w: dict[str, Any]) -> str:
    if "error" in w:
        return f"<p><em>Weather unavailable: {w['error']}</em></p>"

    sunrise = w["sunrise"].split("T")[1] if w.get("sunrise") else "?"
    sunset = w["sunset"].split("T")[1] if w.get("sunset") else "?"

    return f"""
    <p>
      <strong>{w['city']}</strong> — {w['description']}<br>
      Now: <strong>{w['current_temp']}&deg;C</strong>
      &nbsp;|&nbsp; Today: {w['min_temp']}&deg; / {w['max_temp']}&deg;
      &nbsp;|&nbsp; Rain chance: {w['rain_chance']}%<br>
      Humidity: {w['humidity']}% &nbsp;|&nbsp; Wind: {w['wind_kmh']} km/h<br>
      Sunrise {sunrise} — Sunset {sunset}
    </p>
    """


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_weather())
