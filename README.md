# Strabo

Strabo Geolocator by [Asko Nivala](http://askonivala.github.io).

# Installation

Strabo is dependent on the following libraries:
* [GeoPy](https://github.com/geopy/geopy)
* [NLTK](http://www.nltk.org)
* [geojson](https://pypi.python.org/pypi/geojson/)

# Use

Usage: ./strabo.py text.txt

Strabo is using English StanfordNERTagger to tag place names in the text. The path of the geotagger is 
hardcoded, please change this. If the coordinates of the place are not found from its cache, it will search 
it with the selected geocoder and save the results. It will output the list of places as a CSV table with 
latitude and longitude and as a geojson-file. The latter will include the context as a [Leaflet](http://leafletjs.com) popup.  
Consider renaming these files, since rerunning Strabo will overwrite them.

# Known issues

[Nominatim geocoder is not working anymore](https://github.com/geopy/geopy/issues/185) with the current 
version of GeoPy. Use Google until they fix the problem.
