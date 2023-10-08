from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///locations.db")


@app.route("/", methods=["GET"])
def index():
    pocasi = db.execute("select * from locations")
    for slovnik in pocasi:
        latitude = slovnik['latitude']
        longitude = slovnik ['longitude']
        teplota = weather (latitude,longitude)
        slovnik ['teplota'] = teplota

    return render_template("index.html" ,weather_s =pocasi)


def weather(latitude,longitude):
    PARAMS = {'latitude':latitude, 'longitude':longitude, 'hourly':'temperature_2m', 'current_weather':True}
    response = requests.get (url ='https://api.open-meteo.com/v1/forecast', params = PARAMS)
    data = response.json()
    # print (data)
    current_weather = data['current_weather']
    temperature = current_weather['temperature']
    return temperature

