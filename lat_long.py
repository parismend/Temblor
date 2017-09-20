import geopy as gp
from geopy.geocoders import Nominatim

geolocator= Nominatim()

#Dirección debe ser de la forma "Num Calle Ciudad"

def obtain_latlong(dir):
	location = geolocator.geocode(dir)
	lat = location.latitude
	lon = location.longitude
	return lat,lon

if __name__ : '__main__':
	lat,lon = obtain_latlon()


	