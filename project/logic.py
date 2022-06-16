import random
import uuid
from dbaccess import *
import re
from datetime import *
# import pandas as pd
import math
import dataclasses
import json



def GenerateUUID():
    new_uuid = uuid.uuid1()
    string_uuid = str(new_uuid)        
    fixed_uuid = '9E18' + string_uuid[19:23]
    upper_string = fixed_uuid.upper()
    return upper_string
    

    
def IsEmailValid(email):
    pattern = re.compile("^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$")
    return pattern.match(email)

def IsCPRValid(cpr):
    if(len(cpr) == 10):
        return True
    else:
        return False

def GetAccounts():
    accounts = GetAllAccounts()
    return accounts

def GetActiveRoles():
    roles = GetRoles()
    print(roles)
    return roles

def GetParkingSpots():
    spots = GetSpots()
    for spot in spots:
        if spot.type == 1:
            spot.type = 'Staff'
        elif spot.type == 2:
            spot.type = 'Student'
        elif spot.type == 3:
            spot.type = 'Guest'

    return spots

def InsertNewPerson(fname, lname, email, cpr, role_id):
    modified = CreateNewPerson(fname, lname, email, cpr, role_id)
    return modified

def GetRoleFromPbizz(serial):
    return 2
        
def GetParkingSpot():
    spot = GetSpot(1, 2)
    print(f'Spot data: {spot}')

def ChangeSpotStatus(spot_number, spot_type, occupied):
    modified = SetSpotStatus(spot_number, spot_type, occupied)

def RegisterEntrance(parkbizz_serial, timestamp):
    #latest = GetLatestActivity()
    InsertEntrance(parkbizz_serial, timestamp)
    return

def RegisterExit(parkbizz_serial, timestamp):
    exit = ParkingActivity(parkbizz_serial, timestamp, 'EXIT')
    CalculatePayment(parkbizz_serial, exit)
    # receipt
    InsertExit(parkbizz_serial, timestamp)
    return


def CalculatePayment(parkbizz_serial, exit):
    entrance = GetLatestEntrance(parkbizz_serial)
    print(f'Entrance: {entrance}')
    print(f'Exit: {exit}')
    diff = exit.time - entrance.time
    hours = math.floor(diff.total_seconds() / 60 / 60)

    # cap at 8
    if hours > 8:
        hours = 8
    
    if hours < 0:
        hours = 0

    payment = 4 + (4 * hours)
    InsertReceipt(GetAccountNumber(parkbizz_serial), 30, entrance.time, exit.time, exit.time, payment)

def GenerateBizzActivity(serial):
    start_date = datetime(2022, 3, 12, 8, 0, 0)
    for i in range(random.randint(5, 20)): # how many days the activity is going to span
        daily_activity = random.randint(1, 3) # how many times per day
        time_now = start_date + timedelta(minutes=random.randint(30, 180))
        for j in range(daily_activity):
            RegisterEntrance(serial, time_now)
            time_now = time_now + timedelta(minutes=random.randint(30, 180))
            RegisterExit(serial, time_now)
            time_now = time_now + timedelta(minutes=random.randint(30, 180))
        start_date = start_date + timedelta(days=1)
        
def GetAllParkingBizzes():
    return GetParkingBizzes()
    
def GenerateParkbizzes():
    accounts = GetAccounts()
    for account in accounts:
        serial = GenerateUUID()
        expiry = datetime(2025, 6, 15, 8, 0, 0)
        active = True
        InsertParkbizz(serial, active, expiry, account.account_number)
    
def GenerateParkbizzes():
    accounts = GetAccounts()
    for account in accounts:
        serial = GenerateUUID()
        expiry = datetime(2025, 6, 15, 8, 0, 0)
        active = True
        InsertParkbizz(serial, active, expiry, account.account_number)

def GenerateParkingActivity():
    bizzes = GetParkingBizzes()
    for bizz in bizzes:
        GenerateBizzActivity(bizz.serial_number)

# List of ParkingActivity(type - ENTRANCE or EXIT, time: datetime)
def GetParkingActivity(parkbizz_serial):
    return GetLatestActivity(parkbizz_serial)

<<<<<<< Updated upstream
def FlipOccupiedStatus(type, number):
    FlipStatus(type, number)

def DataclassListToJson(list):
    list_dict = []
    for item in list:
        list_dict.append(dataclasses.asdict(item))
    return json.dumps(list_dict)

def UpdateSpotStatus(spot_type, spot_number, occupied):
    UpdateSpot(spot_type, spot_number, occupied)
=======
def GetReceipts(account_number):
    return GetReceiptsFromSerial(account_number)
>>>>>>> Stashed changes


