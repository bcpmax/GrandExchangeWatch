import urllib2
import json
import datetime
import dbmanager
import time
import thread
BASE = "http://services.runescape.com/"
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'GenExcPriceUpdater /1.0 klokeman3@gmail.com')]

def formatRequest(itemID):
    req = "m=itemdb_rs/api/catalogue/detail.json?item={}".format(itemID)
    return BASE + req

def priceToInt(price):
    price = str(price)
    price = price.replace(',','')
    if price[-1].isalpha():
        end = price[-1]
        front_float = float(price[:-1])
        multiple = 1
        if end == 'k':
            multiple = 1000
        elif end == m:
            multiple = 1000000
        price = front_float*multiple
    price = int(price)
    return price 

def get_json(i):
    raw_json = opener.open(formatRequest(int(i))).read()
    while not raw_json:
        time.sleep(3)
        raw_json = opener.open(formatRequest(int(i))).read()
    return raw_json

def update_id(item_id):
    raw_json = get_json(item_id)
    item_dict = json.loads(raw_json)
    current_price = priceToInt(item_dict['item']['current']['price'])
    time_now = datetime.datetime.now().isoformat()
    dbmanager.addPrice(item_id, time_now, current_price)
    print("{}: DONE".format(item_id))

def updateThreaded():
    ids = open("item_id.txt","r")
    lines = ids.readlines()
    ids.close()
    for line in lines:
        itemAttrs = line.split(":")
        i = itemAttrs[0]
        name = itemAttrs[1]
        if name.lower() != "dne\n":
            print("NAME:{}".format(name))
            thread.start_new_thread(update_id,(i,))
    
def update():
    ids = open("item_id.txt","r")
    lines = ids.readlines()
    ids.close()
    for line in lines:
        itemAttrs = line.split(":")
        i = itemAttrs[0]
        name = itemAttrs[1]
        if name.lower() != "dne\n":
            print("NAME:{}".format(name))
            raw_json = get_json(i)
            item_dict = json.loads(raw_json)
            current_price = priceToInt(item_dict['item']['current']['price'])
            time_now = datetime.datetime.now().isoformat()
            dbmanager.addPrice(i, time_now, current_price)
            print(current_price)

if __name__ == "__main__":
    updateThreaded()
