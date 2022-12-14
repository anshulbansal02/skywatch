import requests

API_URL = "http://api.ipify.org/"


def get_public_ip():
    return requests.get(API_URL).text
