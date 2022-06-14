import psycopg2
from dataclasses import dataclass


conn = None

@dataclass
class ParkingSpot:
    """Class for keeping track of an item in inventory."""
    type: str
    number: int
    occupied: bool

    def __init__(self, type: str, number: int, occupied: bool):
        self.type = type
        self.number = number
        self.occupied = occupied

def GetConnection():
    try:
        # conn = psycopg2.connect("dbname=zbcparking user=postgres password=password")

        conn = psycopg2.connect(
            host="10.108.149.16",
            database="parking_lot",
            user="root",
            password="root",
            port="5432"
        )
        
        if conn is not None:
            return conn
        else:
            return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def CreateNewPerson(fname, lname, email, role_id):
    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO people (fname, lname, email, role_id) VALUES(%(fname)s, %(lname)s, %(email)s, %(role_id)s)', {'fname': fname, 'lname': lname, 'email': email, 'role_id': role_id})
        modified = cur.rowcount > 0
        conn.commit()

        return modified
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def SetSpotStatus(spot_number, spot_type, occupied):
    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute('UPDATE parking_spots SET occupied = %(occupied)s WHERE spot_number = %(spot_number)s AND spot_role_type = %(spot_type)s', {'occupied': occupied, 'spot_number': spot_number, 'spot_type': spot_type})
        modified = cur.rowcount > 0
        conn.commit()

        return modified
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def GetSpot(type, number):
    try:
        conn = GetConnection()
        cur = conn.cursor()

        cur.execute('SELECT * from parking_spots where spot_number = %(number)s AND spot_role_type = %(type)s', {'number': number, 'type': type})
        spot = cur.fetchone()

        return spot

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def GetSpots():

    try:
        conn = GetConnection()
        
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        cur.execute("SELECT spot_number, occupied, spot_role_type FROM parking_spots")
        spots = []

        rows = cur.fetchall()

        for row in rows:
            spot = ParkingSpot(row[2], row[0], row[1])

            spots.append(spot)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return spots