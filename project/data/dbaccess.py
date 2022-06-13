import psycopg2


conn = None

try:

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect("dbname=zbcparking user=postgres password=")
     
    # create a cursor
    cur = conn.cursor()
    
# execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    cur.execute("SELECT spot_id, parkbizz_serial, spot_role_type FROM parking_spots")
    print("The number of spots: ", cur.rowcount)

    rows = cur.fetchall()
    for row in rows:
        print(row[1])

  
    
# close the communication with the PostgreSQL
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')
