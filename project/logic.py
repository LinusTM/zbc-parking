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
        

