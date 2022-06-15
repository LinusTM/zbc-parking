import psycopg2
from dataclasses import dataclass
import datetime

conn = None

@dataclass
class ParkingActivity:
    parkbizz_serial: str
    time: datetime
    type: str

    def __init__(self, parkbizz_serial: str, time: datetime, type: str):
        self.parkbizz_serial = parkbizz_serial
        self.time = time
        self.type = type


@dataclass
class Parkbizz:
    serial_number: str
    active: bool
    expiry_date: datetime
    account_number: int

    def __init__(self, serial_number: str, active: bool, expiry_date: datetime, account_number: int):
        self.serial_number = serial_number
        self.active = active
        self.expiry_date = expiry_date
        self.account_number = account_number

@dataclass
class ParkingSpot:
    type: str
    number: int
    occupied: bool

    def __init__(self, type: str, number: int, occupied: bool):
        self.type = type
        self.number = number
        self.occupied = occupied

@dataclass
class Role:
    name: str
    id: int

    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

@dataclass
class Account:
    account_number: int
    balance: float
    active: bool
    person_cpr: str
    owner_fname: str
    owner_lname: str

    def __init__(self, account_number: int, balance: float, active: bool, person_cpr: str, owner_fname: str, owner_lname: str):
        self.account_number = account_number
        self.balance = balance
        self.active = active
        self.person_cpr = person_cpr
        self.owner_fname = owner_fname
        self.owner_lname = owner_lname

def GetConnection():
    try:
        #conn = psycopg2.connect("dbname=zbcparking user=postgres password=password")

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


def GetAllAccounts():
    try:
        conn = GetConnection()
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        cur.execute("SELECT accounts.account_number, accounts.balance, accounts.active, accounts.person_cpr, people.fname, people.lname FROM accounts INNER JOIN people ON accounts.person_cpr = people.cpr_number")
        accounts = []

        rows = cur.fetchall()

        for row in rows:
            account = Account(row[0], row[1], row[2], row[3], row[4], row[5])  
            accounts.append(account)
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return accounts


def GetRoles():
    try:
        conn = GetConnection()
        
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        cur.execute("SELECT * FROM roles")
        roles = []

        rows = cur.fetchall()

        for row in rows:
            role = Role(row[1], row[0])
            roles.append(role)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return roles


def CreateNewPerson(fname, lname, email, cpr, role_id):
    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO people (fname, lname, email, cpr_number, role_id) VALUES(%(fname)s, %(lname)s, %(email)s, %(cpr)s, %(role_id)s)', {'fname': fname, 'lname': lname, 'email': email, 'cpr': cpr, 'role_id': role_id})
        modified = cur.rowcount > 0
        conn.commit()

        return modified
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def GetParkingBizzes():

    try:
        conn = GetConnection()
        
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        cur.execute("SELECT * FROM parkbizz")
        bizzes = []

        rows = cur.fetchall()

        for row in rows:
            bizz = Parkbizz(row[0], row[1], row[2], row[3])
            bizzes.append(bizz)
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return bizzes


def InsertParkbizz(serial, active, expiry, account_number):
    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO parkbizz(serial_number, active, expiry_date, account_number) VALUES(%(serial)s, %(active)s, %(expiry)s, %(account_number)s)', {'serial': serial, 'active': active, 'expiry': expiry, 'account_number': account_number})
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

def InsertEntrance(parkbizz_serial, timestamp):
    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO entrances(parkbizz_serial, time) VALUES (%(parkbizz_serial)s, %(timestamp)s)', {'parkbizz_serial': parkbizz_serial, 'timestamp': timestamp})
        modified = cur.rowcount > 0
        conn.commit()

        return modified
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def InsertExit(parkbizz_serial, timestamp):
    try:
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute('INSERT INTO exits(parkbizz_serial, time) VALUES (%(parkbizz_serial)s, %(timestamp)s)', {'parkbizz_serial': parkbizz_serial, 'timestamp': timestamp})
        modified = cur.rowcount > 0
        conn.commit()

        return modified
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def GetLatestActivity(parkbizz_serial):
    try:
        conn = GetConnection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM entrances WHERE parkbizz_serial = %(parkbizz_serial)s ORDER BY time ASC', {'parkbizz_serial': parkbizz_serial})
        entrances = []

        rows = cur.fetchall()

        for row in rows:
            entrance = ParkingActivity(row[0], row[1], 'ENTRANCE')
            entrances.append(entrance)


        cur.execute('SELECT * FROM exits WHERE parkbizz_serial = %(parkbizz_serial)s ORDER BY time ASC', {'parkbizz_serial': parkbizz_serial})
        exits = []

        rows = cur.fetchall()

        for row in rows:
            exit = ParkingActivity(row[0], row[1], 'EXIT')
            exits.append(exit)



        mixed = []
        index = 0
        for ent in entrances:
            mixed.append(entrances[index])
            mixed.append(exits[index])
            index = index + 1
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return mixed

def GetLatestEntrance(parkbizz_serial):
    try:
        conn = GetConnection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM entrances ORDER BY time DESC LIMIT 1')
        entrance = cur.fetchone()

        return entrance

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()

def GetLatestExit(parkbizz_serial):
    try:
        conn = GetConnection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM exits ORDER BY time DESC LIMIT 1')
        exit = cur.fetchone()

        return exit

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