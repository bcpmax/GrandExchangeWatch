# GE ANALYSIS
import sqlite3
import datetime
import pylab

conn = sqlite3.connect("geprices.db")
cur = conn.cursor()

def select(members = True):
    command = "SELECT items.name, prices.time, prices.price FROM items INNER JOIN prices ON items.id=prices.id"
    if not members:
        command += " WHERE items.members IS 0"
        
    resp = [r for r in cur.execute(command)]
    return resp

def convert_date(date_string):
    date_object = datetime.datetime.strptime(date_string.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    return date_object

def create_dict(list_of_prices):
    prices = {}
    for p in list_of_prices:
        name, date_string, price = p
        date = convert_date(date_string)
        price = int(price)
        if name not in prices.keys():
            prices[name] = []
        prices[name].append((date, price))
    return prices

if __name__ == "__main__":
    price_dict = create_dict(select())
    colors = ['r','g','b','y','k']
    for index, key in enumerate(price_dict.keys()):
        dates = [e[0] for e in price_dict[key]]
        prices =[e[1] for e in price_dict[key]]
        if not all([p == prices[0] for p in prices]):
            print(key)
            print (dates)
            print (prices)
    
