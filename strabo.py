#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Strabo Geolocator by Asko Nivala (aeniva@utu.fi)

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re
import csv, codecs, cStringIO

from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
from time import sleep

# Initializing database for cache
print
print ('Strabo Geolocator by Asko Nivala (aeniva@utu.fi)')
print
print ('Loading database for cache...')
import geopy
import pickle
import sqlite3

class Cache(object):
    def __init__(self, fn='cache.db'):
       self.conn = conn = sqlite3.connect(fn)
       cur = conn.cursor()
       cur.execute('CREATE TABLE IF NOT EXISTS '
                   'Geo ( '
                   'address STRING PRIMARY KEY, '
                   'location BLOB '
                   ')')
       conn.commit()

    def address_cached(self, address):
        cur = self.conn.cursor()
        cur.execute('SELECT location FROM Geo WHERE address=?', (address,))
        res = cur.fetchone()
        if res is None: return False
        return pickle.loads(res[0])

    def save_to_cache(self, address, location):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO Geo(address, location) VALUES(?, ?)',
                    (address, sqlite3.Binary(pickle.dumps(location, -1))))
        self.conn.commit()
print ('Loaded.')

print
print "Choose which Geocoder to use:"
print "1. Nominatim"
print "2. Google (default)"
print
choice = raw_input('Enter your choice [1-2]: ')
choice = int(choice)
if choice == 1:
	geolocator = Nominatim()
elif choice == 2:
	geolocator = GoogleV3()
else:
	geolocator = GoogleV3()

# Pass the argument to filename
filename = sys.argv[-1]

# If no filename is given terminate the program
if filename == "./strabo.py":
	print
	print "Usage: ./strabo.py filename.txt"
	print
	sys.exit()

# Initializing CSV-writer for output.
class excel_semicolon(csv.excel):
	delimiter = ';'
	escapechar = "%"

csv.register_dialect("excel-semicolon", excel_semicolon)

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=excel_semicolon, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

records = []
cache = Cache('test.db')

# Open file
g = open(filename, "r")
text = g.read()
g.close()

# Find tags
output  = re.compile('<LOCATION>(.*?)</LOCATION>', re.DOTALL |  re.IGNORECASE).findall(text)
for index, item in enumerate(output):
#	print item,
	name = item
	address = item

# Routine for geolocator
	location = cache.address_cached(address)
	if location:
		print ('Was cached: '),
	else:
		print('Was not cached, looking up and caching now... '),
		location = geolocator.geocode(output[index], timeout=10)
		cache.save_to_cache(address, location)
	try:
		print(address, location.latitude, location.longitude)
		lat = str(location.latitude)
		longi = str(location.longitude)
		latlong = lat + ',' + longi
		records.append({
				'name': item,
				'latlong': latlong
	#			'lat': lat,
	#			'long': longi,
			})
	except:
		print "(Geocoding failed.)"
		# TODO: Save these results in separate list to debug OCR-errors and historical places.
		continue

	sleep(1)

# Write the tags to CSV table
with open('output.csv', 'w') as csvfile:
	writer = UnicodeWriter(csvfile, quoting=csv.QUOTE_NONE)
	writer.writerow(["City;Latlong"])
	for record in records:
#		writer.writerow([record['name'], record['lat'], record['long']])
		writer.writerow([record['name'], record['latlong']])
