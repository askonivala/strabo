# Strabo

Strabo Geolocator by [Asko Nivala](http://askonivala.github.io).

# Installation

Strabo is dependent on [GeoPy](https://github.com/geopy/geopy)-library. Assuming you have [PIP](https://pip.pypa.io/en/latest/installing/) installed, 
open the terminal and type "pip install geopy".

# Use

Usage: ./strabo.py text.txt

Strabo is assuming that you have marked all places with `<LOCATION>`-tags like this: `<LOCATION>Paris</LOCATION>.` If the place is not found from its 
cache, it will search it with the selected geocoder and save the results. It will output the list of places as a CSV table with latitude and 
longitude. Consider renaming the CSV file, because rerunning Strabo will overwrite output.csv.

# Known issues

[Nominatim geocoder is not working anymore](https://github.com/geopy/geopy/issues/185) with the current version of GeoPy. Use Google 
until they fix the problem.
