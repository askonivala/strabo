# Strabo

Strabo Geolocator by [Asko Nivala](http://askonivala.github.io).

Usage: ./strabo.py text.txt

Strabo is assuming that you have marked all places with `<LOCATION>`-tags like this: `<LOCATION>Paris</LOCATION>.` It will output the 
list of places as a CSV table with latitude and longitude.

# Known issues

[Nominatim geocoder is not working anymore](https://github.com/geopy/geopy/issues/185) with the current version of GeoPy. Use Google 
until they fix the problem.

# TODO

A cache for searched locations.
