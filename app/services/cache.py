import redis
import json
import os

r_host = os.getenv("REDIS_HOST") or "localhost"
r_port = os.getenv("REDIS_PORT") or "6379"
r_pass = os.getenv("REDIS_PASS") or ""

cache = redis.Redis(host=r_host, port=r_port, password=r_pass)


class LocationCache:
    def __init__(self):
        self.ttl = 3600  # 1 hour

    def get(self, ip):
        cached = cache.get(f"ip:{ip}")
        if cached:
            return json.loads(cached)

    def set(self, ip, location):
        cache.set(f"ip:{ip}", json.dumps(location), self.ttl)


class WeatherCache:
    def __init__(self):
        self.ttl = 60  # 1 minute

    def get(self, coords):
        cached = cache.get(f"weather:{coords['lon']}:{coords['lat']}")
        if cached:
            return json.loads(cached)

    def set(self, coords, weather_data):
        cache.set(
            f"weather:{coords['lon']}:{coords['lat']}",
            json.dumps(weather_data),
            self.ttl,
        )
