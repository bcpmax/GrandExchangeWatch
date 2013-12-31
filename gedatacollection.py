import urllib2
import json
import time
import dbmanager
BASE = "http://services.runescape.com/"

def formatRequest(itemID):
    req = "m=itemdb_rs/api/catalogue/detail.json?item={}".format(itemID)
    return BASE + req


last_found = -1
try:
    id_file = open("item_id.txt", 'r')
    last_found = int(id_file.readlines()[-1].split(":")[0])
except IOError:
    print("New file created")
    id_file = open("item_id.txt", 'w')
finally:
    id_file.close()

id_file = open("item_id.txt", 'a')
try:
    for i in range(9999):
        if i > last_found:
            entry = ""
            try:
                url = formatRequest(i)
                webtext = urllib2.urlopen(url).read()
                while not webtext:
                    time.sleep(1)
                    webtext = urllib2.urlopen(url).read()
                # if sucessful 
                json_item_dict = json.loads(webtext)
                name = json_item_dict['item']['name'].replace("'","")
                isMember = json_item_dict['item']['members'] == 'true'
                entry = "{}:{}:{}".format(i, name, isMember)

                dbmanager.addItem(str(name), i, isMember)
                
            except (urllib2.HTTPError):
                entry = "{}:{}".format(i, "DNE")
            print entry
            id_file.write(entry + "\n")
        
finally:
    id_file.close()
