#!/usr/bin/env python3
from flask import Flask, render_template
from registration import registration
from logic import *
import json

app = Flask(__name__)

app.register_blueprint(registration)

@app.route("/")
def main_page():
   #GetParkingSpot()
   # ChangeSpotStatus(5, 1, True)
   # print(GetSpot(1, 5))
   # InsertNewPerson('carlo', 'ms', 'carletto@gmail.com', 2)
   spots = GetParkingSpots()  
   return render_template("parking.html", spots=spots)

@app.route("/data/spots")
def get_spots():
   spots = GetParkingSpots()
   spotsj = json.dumps(list(spots))
   return spotsj

if __name__ == "__main__":
    app.run(debug=True)