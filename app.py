from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///locations.db")


@app.route("/", methods=["GET", "POST"])
def index():
    weather = db.execute("select * from locations")
    return render_template("index.html" ,weather_s =weather)
