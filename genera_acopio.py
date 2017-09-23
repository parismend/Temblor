#Correr desde HOME

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import httplib2
import argparse
import pandas as pd
import geopy as gp
from geopy.geocoders import Nominatim
import numpy as np
from oauth2client.file import Storage
from df2gspread import df2gspread as d2g
import logging


try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'Downloads/secreto_cliente.json'
APPLICATION_NAME = 'Descargas'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_Data_temblor(idsheet, rangesheet):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
#    spreadsheetId = 'Necesidades de Zonas Afectadas y Albergues '
    spreadsheetId = 'Centros de Acopio'
    #####DAÑOS Y DERRUMBES VERIFICADOS
    #####Para descargar otras páginas cambiar el nombre en el campo range
    result = service.spreadsheets().values().get(
        spreadsheetId=idsheet,
        range=rangesheet).execute()
    values = result.get('values', [])
    return pd.DataFrame(values)

geolocator= Nominatim()

#Dirección debe ser de la forma "Num Calle Ciudad"
def dir_correct(calle, numero, ciudad):
	k = []
	k.append(numero)
	k.append(calle)
	if pd.isnull(ciudad):
		k.append('cdmx')
	else:
		k.append(ciudad)
	dirr =' '.join(k)
	return dirr
    

def obtain_latlong(dirr):
    location = geolocator.geocode(dirr)
    lat = location.latitude
    lon = location.longitude
    return lat,lon
        

def get_latlon(df):
    #calles = df['Calle'].tolist()
    #numeros = df['Número Exterior  o Aproximado (escribe sólo el número)'].tolist()
	calle=df['Calle'].tolist()
	numero=df['Número (aproximado al menos)'].tolist()
	ciudad=df['Estado '].tolist()
	colonia=df['Colonia'].tolist()
	delegacion=df['Delegación o municipio'].tolist()
	lati = []
	longi = []
    #dirr=dir_correct(calle, numero)
    #lat,lon = obtain_latlong(dirr)
	for i in range(df.shape[0]):
		try:    
			lat_aux, lon_aux = obtain_latlong(dir_correct(calle[i], str(numero[i]),
				 ciudad[i]))
		except:
			lat_aux=''
			lon_aux=''
		lati.append(lat_aux)
		longi.append(lon_aux)
		print(lat_aux, lon_aux)
	df['latitud']=lati
	df['longitud']=longi
	return df


if __name__ == '__main__':

	acopio=pd.read_csv('~/Downloads/Centros de Acopio.csv')
	acopio=get_latlon(acopio)
	acopio.columns=['Marca temporal', 'Nombre del centro', 'Calle', 'Número aprox', 'Colonia', 'Delegacion', 
		'contacto', 'Telefono', 'Articulos Urgentes', 'Alimentos Faltantes', 'Alimentos Existentes', 
		'Medicamentos Faltantes', 'Medicamentos Existentes', 'Herramientas Faltantes', 'Herramientas Existentes', 
		'Otros Articulos', 'Horarios de Atencion', 'Se requieren Voluntarios', 'Verificado', 'Estado',
		 'Especialistas Faltantes', 'Especialista Existentes', 'latitud', 'longitud']
	acopio.to_csv('acopio.csv', encoding= 'utf-8')

