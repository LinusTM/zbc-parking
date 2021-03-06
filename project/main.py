#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request
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

@app.route("/admin/people")
def people():
   people = GetAllPeople()
   return render_template("people.html", people = people)
    
@app.route("/admin/accounts")
def accounts():
   accounts = GetAccounts()
   return render_template("accounts.html", accounts = accounts)

@app.route("/data/spots")
def get_spots():
   spots = GetParkingSpots()
   return DataclassListToJson(spots)

# Takes post request for changing occupied status from parking spots
@app.route("/data/api", methods=['POST'])
def post_park():
   record = json.loads(request.data)
   spot_number = record['spot_number']
   spot_type = record['spot_type']
   spot_occupied = record['occupied']
   ChangeSpotStatus(spot_number, spot_type, spot_occupied)
   return jsonify(record)

# Receives receipts related to account
@app.route("/data/receipts", methods=['GET'])
def get_receipts():
   account_number = request.args.get('account_number')
   receipts = GetReceipts(account_number)
   return jsonify(receipts)


@app.route("/model/scanner", method=['POST'])
def get_scanner():
   content = request.json
   id = content['serialNr']
   number = content['spotNr']
   FlipOccupiedStatus(3, number)

@app.route("/spots/update/<spot_type>/<spot_number>/<occupied>", methods=['POST'])
def update_spot(spot_type, spot_number, occupied):
   if request.is_json:
      print('is json')
   else:
      print('not json')
   # content = request.get_json()
   # print('got content')
   # type = content['spot_type']
   # number = content['spot_number']
   # occupied = content['occupied']
   UpdateSpotStatus(spot_type, spot_number, occupied)
   resp = jsonify(success=True)
   return resp

if __name__ == "__main__":
	app.run(debug=True)
