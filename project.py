import xml.etree.ElementTree as ET
import dateutil.parser
from pprint import pprint 
from pymongo import MongoClient

WEENDAYS = ['SUN', 'MON', 'TUE', 'WED', 'THU',  'FRI', 'SAT']

client = MongoClient()
db = client.mydb
db.osmdb.remove({})

print "Parsing Start!"

fname = 'manhattan.osm'
root = ET.parse(fname).getroot()

print "Parsing Done!"

for child in root.getchildren():
    data = {}
    nodeAttrib = child.attrib
    
    if 'id' not in nodeAttrib:
        continue

    data['id'] = nodeAttrib['id']
    data['type'] = child.tag
    data['user'] = nodeAttrib['user']
    if 'lat' in nodeAttrib and 'lon' in nodeAttrib:
        data['position'] = [float(nodeAttrib['lat']), float(nodeAttrib['lon'])]
    # ISO 8601 Format => datetime object
    dateInfo = dateutil.parser.parse(nodeAttrib['timestamp'])

    # Problem 2
    # Time Information Handling
    dataDic = {}
    dataDic['year'] = dateInfo.year
    dataDic['month'] = dateInfo.month
    dataDic['day'] = dateInfo.day
    dataDic['hour'] = dateInfo.hour
    dataDic['minute'] = dateInfo.minute
    dataDic['dayOfWeek'] = WEENDAYS[dateInfo.weekday()]
    dataDic['YM'] = "{0}-{1:02}".format(dateInfo.year, dateInfo.month)
    dataDic['HM'] = "{0:02}:{1:02}".format(dateInfo.hour, dateInfo.minute)
    data['timeInfo'] = dataDic

    subChildren = child.getchildren()
    if len(subChildren) > 0 :
        # Tag Information 
        tags = {}
        for tagInNode in subChildren:
            if tagInNode.tag == 'tag':
                keyName = tagInNode.attrib['k']
                # MongoDB does not want a key to contain colon, "."
                keyName = keyName.replace('.', ':') 
                value = tagInNode.attrib['v']
                tags[keyName] = value
        data['tags'] = tags

    db.osmdb.insert(data)