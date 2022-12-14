import random
import os
import json

import app.apis as apis
from .cache import LocationCache, WeatherCache


class LocationService:
    cache = LocationCache()

    @classmethod
    def get_ip(cls, request):
        if "X-Forwarded-For" in request.headers:
            ip = str(request.headers["X-Forwarded-For"])
        else:
            ip = str(request.environ.get("HTTP_X_REAL_IP", request.remote_addr))

        if ip == "127.0.0.1":
            ip = apis.get_public_ip()

        return ip

    @classmethod
    def get_location(cls, ip):
        cached_location = cls.cache.get(f"ip:{ip}")
        if cached_location:
            return cached_location

        location = apis.get_geolocation(ip)

        if not location["success"]:
            raise Exception("UserLocationError")
        else:
            location["ip"] = ip
            cls.cache.set(ip, location)
            return location


class WeatherService:
    cache = WeatherCache()

    @classmethod
    def get_weather(cls, location):
        weather = apis.get_weather(location["coords"]["lon"], location["coords"]["lat"])

        cached_weather = cls.cache.get(location["coords"])
        if cached_weather:
            return cached_weather

        if not weather:
            raise Exception("WeatherError")

        weather_data = {
            "temperature": weather["main"]["temp"],
            "feels_like": weather["main"]["feels_like"],
            "condition": weather["weather"][0]["main"],
            "condition_id": weather["weather"][0]["id"],
            "description": weather["weather"][0]["description"],
            "wind": weather["wind"],
            "pressure": weather["main"]["pressure"],
            "humidity": weather["main"]["humidity"],
            "comment": "It's such a nice sunny day outside",
        }

        cls.cache.set(location["coords"], weather_data)
        return weather_data

    @classmethod
    def get_comment(cls, condition):

        comments_file_path = os.getcwd() + "/app/services/comments.json"

        with open(comments_file_path, "r") as comments_file:
            comments = json.loads(comments_file.read())

        return random.choice(comments[condition])
