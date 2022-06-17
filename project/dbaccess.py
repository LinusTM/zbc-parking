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

# Reprensent an account connected to a person and can contain multiple Parkbizz instances  
@dataclass
class Account:
    account_number: int
    balance: float
    active: bool
    person_cpr: str
    parkbizzes: list[Parkbizz]
    # owner_fname: str
    # owner_lname: str

    def __init__(self, account_number: int, balance: float, active: bool, person_cpr: str, parkbizzes: list[Parkbizz]):
        self.account_number = account_number
        self.balance = balance
        self.active = active
        self.person_cpr = person_cpr
        self.parkbizzes = parkbizzes

# Represent a person can contain multiple Account instances
@dataclass
class Person:
    cpr_number: str
    fname: str
    lname: str
    email: str
    role: str
    accounts: list[Account]

    def __init__(self, cpr_number: int, fname: str, lname: str, email : str, role : str, accounts : list[Account]):
        self.cpr_number = cpr_number
        self.fname = fname
        self.lname = lname
        self.email = email
        self.role = role
        self.accounts = accounts

# Represents a receipt holding info for entering and exiting parking lot and the price for the time parkedr
@dataclass
class Receipt:
    receipt_id: int
    account_number: int
    hourly_fee: float
    entrance_time: datetime
    exit_time: datetime
    payment_time: datetime
    total: float
    def __init__(self, receipt_id: int, account_number: int, hourly_fee: float, entrance_time: datetime, exit_time: datetime, payment_time: datetime, total: float):
        self.receipt_id = receipt_id
        self.account_number = account_number
        self.hourly_fee = hourly_fee
        self.entrance_time = entrance_time
        self.exit_time = exit_time
        self.payment_time = payment_time
        self.total = total

def GetConnection():
    try:
        #conn = psycopg2.connect("host=localhost dbname=zbcparking user=postgres password=password")

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

# Recieves all people from database with related accounts and parkbizz connected.
def GetAllPeople():
    try:
        conn = GetConnection()
        
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        cur.execute("SELECT people.cpr_number, people.fname, people.lname, people.email, (SELECT roles.role_name FROM roles WHERE people.role_id = roles.role_id) FROM people")
        people = []

        peopleRows = cur.fetchall()

        for row in peopleRows:
            cur.execute("SELECT accounts.account_number, accounts.balance, accounts.active, accounts.person_cpr FROM accounts WHERE accounts.active = TRUE AND accounts.person_cpr = %(cpr)s", {"cpr" : row[0]})
            accounts = []

            accountRows = cur.fetchall()
            for accRow in accountRows:
                cur.execute("SELECT * FROM parkbizz WHERE parkbizz.active = TRUE AND parkbizz.account_number = %(acc_num)s", {"acc_num" : accRow[0]})
                bizzes = []

                bizzRows = cur.fetchall()
                for bizzRow in bizzRows:
                    bizz = Parkbizz(bizzRow[0], bizzRow[1], bizzRow[2], bizzRow[3])  
                    bizzes.append(bizz)
                account = Account(accRow[0], accRow[1], accRow[2], accRow[3], bizzes)  
                accounts.append(account)

            person = Person(row[0], row[1], row[2], row[3], row[4], accounts)  
            people.append(person)
            
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return people

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
            
            account = Account(row[0], row[1], row[2], row[3])  
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
        print(spot_type)
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

def FlipStatus(spot_type, spot_number):
    try:
        print(spot_type)
        conn = GetConnection()
        cur = conn.cursor()
        cur.execute("UPDATE parking_spots SET occupied = !occupied WHERE spot_number = %(spot_number)s AND spot_role_type = %(spot_type)s'", {'spot_number': spot_number, 'spot_type': spot_type})

        conn.commit()
        return True
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
# Recieves receipt related to account number 
def GetReceiptsFromSerial(account_number):
    try:
        conn = GetConnection()
        cur = conn.cursor()

        cur.execute('SELECT * FROM account_receipts WHERE account_receipts.account_number = %(acc_num)s ORDER BY entrance_time DESC', {"acc_num": account_number})
        rows = cur.fetchall()

        receipts = []

        for row in rows:
            receipt = Receipt(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            receipts.append(receipt)
        
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        cur.close()
        if conn is not None:
            conn.close()
        return receipts
    

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
        cur.execute("SELECT spot_number, occupied, spot_role_type FROM parking_spots ORDER BY spot_role_type ASC, spot_number ASC")
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
