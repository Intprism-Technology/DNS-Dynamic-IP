from ast import Try
from cmath import e
import configuration
import mysql.connector

def DBConnect():
    try:
        conn = mysql.connector.connect(
                host        = configuration.cyberpanel_dbHost,
                user        = configuration.cyberpanel_dbUser,
                password    = configuration.cyberpanel_dbPassword,
                database    = configuration.cyberpanel_dbName
            )
        return conn
    except:
        print("Invalid DB Credentials !!! ")
        exit()

def dns_update(ip_address):
    conn = DBConnect()
    
    db = conn.cursor()
    db.execute("SELECT * FROM records")
    result = db.fetchall()
    for data in result:
        if(data[3] == 'A'):
            if(conn.is_connected() == True):
                sql = "UPDATE records SET content='{}' WHERE name='{}' AND type='A'".format(ip_address, data[2])
                db.execute(sql)
                conn.commit()
                print("UPDATED "+data[2]+" - "+data[4]+" => "+ip_address)
            else:
                print("DB Connect ERROR !!!")
                exit()