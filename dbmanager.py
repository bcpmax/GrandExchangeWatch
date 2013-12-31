# SQLITE
import sqlite3 as sqlite

TABLES = {"items":["id","name","members"],
          "prices":["id", "time", "price"],
          }

def connect():
    """Returns a connection object and a cursor object"""
    conn = sqlite.connect('geprices.db')
    cur = conn.cursor()
    return conn, cur

def create(cursor):
    itemsTable = "create table items (id integer, name text, members integer);"
    pricesTable = "create table prices (id integer, time text, price real);"
    cursor.execute(itemsTable)
    cursor.execute(pricesTable)
    conn.commit()
    
def addItem(name, idnum, members):
    members = 1 if members else 0
    
    conn, cur = connect()
    command = "insert into items values ({},'{}',{});".format(idnum, name, members)
    cur.execute(command)
    conn.commit()
    conn.close()

def addPrice(idnum, time, price):
    conn, cur = connect()
    command = "insert into prices values ({},'{}',{});".format(idnum, time, price)
    cur.execute(command)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    conn, cur = connect()
    create(cur)
    conn.close()
