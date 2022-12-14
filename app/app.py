from flask import Flask, url_for, redirect, render_template, request, session
import os

from app.services import LocationService, WeatherService


app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET") or "random"


@app.route("/")
def index():

    try:
        user_ip = LocationService.get_ip(request)
        location = LocationService.get_location(user_ip)

        session["location"] = location

        state = location["state"].replace(" ", "-")
        city = location["city"].replace(" ", "-")

        return redirect(
            url_for(
                "weather",
                state=state,
                city=city,
            )
        )
    except:
        return redirect(url_for("error"))


@app.route("/weather/<state>/<city>")
def weather(city, state):
    location = session["location"]
    if not location:
        return redirect(url_for("index"))

    try:
        weather_data = WeatherService.get_weather(location)
    except:
        return redirect(url_for("error"))

    return render_template(
        "weather.html",
        location=location,
        weather=weather_data,
    )


@app.errorhandler(404)
def error_page(error):
    return render_template("error.html"), 500


"""
Filters
"""


@app.template_filter()
def trunc_fit(string, max_len=20):
    if len(string) > max_len:
        return string[: max_len - 3] + "..."
    else:
        return string


@app.template_filter()
def to_c(temp):
    return round(273.15 - temp, 0)


@app.template_filter()
def weather_condition(condition_id):
    w = str(condition_id)
    if w.startswith("2"):
        return "thunder"
    elif w.startswith("3"):
        return "drizzle"
    elif w.startswith("5"):
        return "rain"
    elif w.startswith("6"):
        return "snow"
    elif w.startswith("7"):
        return "haze"
    elif condition_id == 800:
        return "sun"
    else:
        return "clouds"


@app.template_filter()
def weather_comment(condition_id):
    condition = weather_condition(condition_id)
    return WeatherService.get_comment(condition)
