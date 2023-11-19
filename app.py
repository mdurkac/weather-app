from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
import datetime

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

@app.route("/new-locations", methods=['GET'])
def new_locations():
    location = request.args.get('q')
    PARAMS = {'name':location, 'count':10}
    response = requests.get (url ='https://geocoding-api.open-meteo.com/v1/search', params = PARAMS) 
    data = response.json()
    if 'results' in data:
        results = data ['results']
        for slovnik in results:
            country_code = slovnik['country_code']
            slovnik['country_code'] = country_code.lower()
        return render_template("new_locations.html", locations=results)
    else:
        return render_template("no_locations_found.html")
    
@app.route("/save_location", methods=['POST'])
def save_location():
    id =request.form.get("id")
    name =request.form.get("name")
    country =request.form.get("country")
    country_code=request.form.get("country_code").lower()
    latitude=request.form.get("latitude")
    longitude=request.form.get("longitude")
    db.execute("INSERT OR IGNORE INTO locations (id, name, country, country_code, latitude, longitude) VALUES (?,?,?,?,?,?)", id, name, country, country_code, latitude, longitude)
    return redirect("/")


@app.route("/delete", methods=['POST'])
def delete():
    id =request.form.get("id")
    if id:
        db.execute("delete from locations where id=?", id)
    return redirect("/")


@app.route("/more_info", methods=['GET'])
def more_info():
    id = request.args.get('id')
    list = db.execute("select * from locations where id=?", id)
    slovnik = list [0]
    latitude = slovnik['latitude']
    longitude = slovnik ['longitude']
    current, daily = get_forecast (latitude, longitude)
    return render_template ('forecast_page.html', location= slovnik, weather=current, days=daily)

def get_forecast(latitude, longitude):
    PARAMS = {'latitude':latitude, 'longitude':longitude,'current':'temperature_2m,apparent_temperature,is_day,rain,showers,windspeed_10m','daily':'temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,rain_sum,showers_sum,windspeed_10m_max', 'timezone':'auto' }
    response = requests.get (url ='https://api.open-meteo.com/v1/forecast', params = PARAMS) 
    data = response.json()
    current = data ['current']
    daily = data ['daily']
    return current, seven_days(daily)


def seven_days(daily):
    new_list = []
    time = daily['time']
    temperature_2m_max = daily ['temperature_2m_max']
    temperature_2m_min = daily ['temperature_2m_min']
    for i in range(0,7,1):
        day = func(time[i])
        slovnik = {'time': day, 'temperature_2m_max': temperature_2m_max[i],'temperature_2m_min': temperature_2m_min[i] }
        new_list.append(slovnik)
    return new_list

def func(date):
    the_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    day = the_date.strftime('%a')
    return day