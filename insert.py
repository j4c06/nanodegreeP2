from pymongo import MongoClient
import json
from pprint import pprint
filename = r'southern_manhattan.json'
with open(filename, 'r') as f:
    rawdata = json.loads(f.read())

client = MongoClient()
db = client.mydb
db.osmdb.remove({})

for k, item in enumerate(rawdata):
    db.osmdb.insert(item)

print  "Done."