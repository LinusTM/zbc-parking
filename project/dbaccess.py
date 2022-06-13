import psycopg2
from dataclasses import dataclass


conn = None

@dataclass
class ParkingSpot:
    """Class for keeping track of an item in inventory."""
    type: str
    number: int
    pbizz_serial: str

    def __init__(self, type: str, number: int, pbizz_serial: int):
        self.type = type
        self.number = number
        self.pbizz_serial = pbizz_serial

def GetConnection():
    try:
        conn = psycopg2.connect("dbname=zbcparking user=postgres password=1H24w87lm")
        if conn is not None:
            return conn
        else:
            return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



def GetSpots():

    try:
        conn = GetConnection()
        
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        cur.execute("SELECT spot_id, parkbizz_serial, spot_role_type FROM parking_spots")
        spots = []

        rows = cur.fetchall()

        for row in rows:
            spot = ParkingSpot(row[2], row[0], row[1])

            spots.append(spot)
        
    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return spots