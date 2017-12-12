import googlemaps
import json
from datetime import datetime



def call_test():
	API_KEY = 'AIzaSyCZNp4cOrpSoYsQ94MOIS0TzPdou2yYLUk'
	gmaps = googlemaps.Client(key=API_KEY)

	# Geocoding an address
	geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
	print(geocode)
	# Look up an address with reverse geocoding
	reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

	# Request directions via public transit
	now = datetime.now()
	directions_result = gmaps.directions("Sydney Town Hall",
	                                     "Parramatta, NSW",
	                                     mode="transit",
	                                     departure_time=now)






if __name__ == '__main__':
	call_test()