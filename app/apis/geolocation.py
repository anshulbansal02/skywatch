import requests

API_URL = "http://ip-api.com/json"


def get_geolocation(ip):
    geo = requests.get(f"{API_URL}/{ip}").json()

    return {
        "success": geo["status"] == "success",
        "city": geo["city"],
        "state": geo["regionName"],
        "coords": {"lon": geo["lat"], "lat": geo["lon"]},
    }
