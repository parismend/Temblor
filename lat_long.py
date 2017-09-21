import geopy as gp
from geopy.geocoders import Nominatim

geolocator= Nominatim()

#Dirección debe ser de la forma "Num Calle Ciudad"
def dir_correct(calle, numero):
	k = []
	k.append(numero)
	k.append(calle)
	k.append('cdmx')
	dirr =' '.join(k)
	return dirr
	


def obtain_latlong(dirr):
	location = geolocator.geocode(dirr)
	lat = location.latitude
	lon = location.longitude
	return lat,lon

if __name__ == '__main__':
	dirr = dir_correct()
	lat,lon = obtain_latlon(dirr)


	
