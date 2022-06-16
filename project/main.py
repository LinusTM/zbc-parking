#!/usr/bin/env python3
from flask import Flask, render_template, request
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
   #GenerateUUIDs()
   spots = GetParkingSpots()  
   return render_template("parking.html", spots=spots)
   #roles = GetActiveRoles()
   #return render_template("registerPerson.html", roles = roles)

@app.route("/parking")
def parking_page():
   spots = GetParkingSpots()  
   return render_template("parking.html", spots=spots)


@app.route("/admin/register/person", methods=['GET', 'POST'])
def register_person():
   if request.method == 'GET':
         roles = GetActiveRoles()
         return render_template("registerPerson.html", roles = roles)
   else:
      fname = request.form['first-name']
      lname = request.form['last-name']
      email = request.form['email']
      role = request.form['role']
      cpr = request.form['cpr-number']

      if(IsCPRValid(cpr) is False):
         return render_template("registerPersonResult.html", success = False, message = 'Invalid CPR Number.')

      if(IsEmailValid(email) is False):
         return render_template("registerPersonResult.html", success = False, message = 'Invalid email format.')
      
      success = InsertNewPerson(fname, lname, email, cpr, role)
      if success is True:
           return render_template("registerPersonResult.html", success = True)
      else:
           return render_template("registerPersonResult.html", success = False, message = "Error inserting new person")

    
@app.route("/admin/accounts")
def accounts():
   accounts = GetAccounts()
   return render_template("accounts.html", accounts = accounts)

@app.route("/data/spots")
def get_spots():
   spots = GetParkingSpots()
   spotsj = json.dumps(list(spots))
   return spotsj

if __name__ == "__main__":
	app.run(debug=True)
