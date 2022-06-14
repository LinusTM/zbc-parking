from random import getstate
import uuid
from dbaccess import *

def GenerateUUIDs():
    uuids = []
    for i in range(10):
        new_uuid = uuid.uuid1()
        string_uuid = str(new_uuid)
        fixed_uuid = string_uuid[0:4] + string_uuid[19:23]
        uuids.append(fixed_uuid)
        print(fixed_uuid)
    

    
def GetActiveRoles():
    roles = GetRoles()
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

def InsertNewPerson(fname, lname, email, role_id):
    modified = CreateNewPerson(fname, lname, email, role_id)
    return modified

def GetRoleFromPbizz(serial):
    return 2
        
def GetParkingSpot():
    spot = GetSpot(1, 2)
    print(f'Spot data: {spot}')

def ChangeSpotStatus(spot_number, spot_type, occupied):
    modified = SetSpotStatus(spot_number, spot_type, occupied)



