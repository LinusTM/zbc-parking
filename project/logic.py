from random import getstate

from dbaccess import *



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



