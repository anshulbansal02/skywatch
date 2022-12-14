import requests
import os


API_KEY = os.getenv("WEATHER_API_KEY") or "2cf8ce83856c9385c237649dbcd612f9"
API_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(lon, lat):
    res = requests.get(API_URL, params={"lat": lat, "lon": lon, "appid": API_KEY})
    return res.json()
