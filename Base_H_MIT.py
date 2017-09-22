import pandas as pd
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import re
import os
import httplib2
from geopy.geocoders import Nominatim
from Dicc_Tipo_Danhos import camb_tipos

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'creds/secreto_cliente.json'
APPLICATION_NAME = 'Temblor'

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
    credential_path = os.path.join(
        credential_dir,
        'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_Data_temblor():
    """Shows basic usage of the Sheets API.
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets',
                              'v4',
                              http=http,
                              discoveryServiceUrl=discoveryUrl)
    # DAÑOS Y DERRUMBES VERIFICADOS
    # Para descargar otras páginas cambiar el onmbre en el campo range
    result = service.spreadsheets().values().get(
        spreadsheetId='1vHrM6r3sO1f6ylsci_B7z08PrLsYKpG5VywjZXD6l5M',
        range='Form Responses 1!A1:AH10000').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values


def insert_Data_temblor(datos):
    """Shows basic usage of the Sheets API.
    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets',
                              'v4',
                              http=http,
                              discoveryServiceUrl=discoveryUrl)
    result = service.spreadsheets().values().get(
        spreadsheetId='1wLHf5ITtTsfErWoPHwhu7Vfy-96eQKKxZO2AmZbP9XY',
        range='Datos!A1:H10000').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print(values)


def estructura_sheet(listas):
    columnas = listas[0]
    info = pd.DataFrame()
    for lista in listas:
        dicc_aux = {}
        for col in range(len(lista)):
            dicc_aux[columnas[col]] = lista[col]
        info = info.append(dicc_aux, ignore_index=True)
    return info

if __name__ == '__main__':

data = get_Data_temblor()
harvard_mit = estructura_sheet(data)

#harvard_mit = pd.read_csv('/Users/parismendez/Desktop/Manos.csv')


Calle = [''  for x in range(0,len(harvard_mit))]
Colonia = harvard_mit['Colonia']
Delegacion = harvard_mit['Delegación/municipio']
Estado = harvard_mit['Estado']
Foto = [''  for x in range(0,len(harvard_mit))]
Herramientas_Faltantes = [''  for x in range(0,len(harvard_mit))]
Herramientas_Sobrantes = [''  for x in range(0,len(harvard_mit))]
Hora = [''  for x in range(0,len(harvard_mit))]
Hora_Reporte = [''  for x in range(0,len(harvard_mit))]
Mano_Faltante = [''  for x in range(0,len(harvard_mit))]
Mano_Sobrantes = [''  for x in range(0,len(harvard_mit))]
Medicamentos_Faltantes = [''  for x in range(0,len(harvard_mit))]
Medicamentos_Sobrantes = [''  for x in range(0,len(harvard_mit))]
Numero_Exterior_Aproximado = [''  for x in range(0,len(harvard_mit))]
Numero_Personas_Atrapadas = [''  for x in range(0,len(harvard_mit))]
Numero_Personas_Desaparecidas = [''  for x in range(0,len(harvard_mit))]
Numero_Personas_Fallecidas = [''  for x in range(0,len(harvard_mit))]
Numero_Personas_Lesionadas = [''  for x in range(0,len(harvard_mit))]
Numero_Personas_Rescatadas = [''  for x in range(0,len(harvard_mit))]
Otra_Referencia_Ubicacion = harvard_mit['Comentarios / Información adicional']
Timestamp = harvard_mit['Timestamp']
ddd = harvard_mit['Timestamp']
ddd = pd.to_datetime(ddd)
eee = []
x=0
while x < len(ddd):
	eee.append(ddd[x].hour)
	x = x+1
fff = []
y = 0
while y < len(eee):
	fff.append(eee[y]-1)
	y = y+1
z = 0
while z < len(fff):
	if fff[z]<0:
		fff[z]=23
	ddd[z].replace(hour=fff[z])
	z = z+1
Timestamp = ddd

Tipo_Infraestructura = [''  for x in range(0,len(harvard_mit))]
Tipo_de_Uso = [''  for x in range(0,len(harvard_mit))]
Tipo_del_Danio = harvard_mit['Ofrezco/Necesito']
Verificado = [''  for x in range(0,len(harvard_mit))]
Viveres_Faltantes = harvard_mit['¿Qué ofrezco/necesito? (comida, hospedaje, agua, transporte, peritajes, etc.) - Por favor ofrece ayuda profesional (asistencia médica, peritajes) si eres un profesional en el tema']
Viveres_Sobrantes = [''  for x in range(0,len(harvard_mit))]
latitud = harvard_mit['Latitude']
longitud = harvard_mit['Longitude']


Har_Mit = pd.DataFrame({
'Calle': Calle,
'Colonia': Colonia,
'Delegación': Delegacion,
'Estado' : Estado,
'Foto': Foto,
'Herramientas Faltantes': Herramientas_Faltantes,
'Herramientas Sobrantes': Herramientas_Sobrantes,
'Hora': Hora,
'Hora del Reporte': Hora_Reporte,
'Mano de Obra Faltante': Mano_Faltante,
'Mano de Obra Sobrantes': Mano_Sobrantes,
'Medicamentos Faltantes': Medicamentos_Faltantes,
'Medicamentos Sobrantes': Medicamentos_Sobrantes,
'Número Exterior  o Aproximado': Numero_Exterior_Aproximado,
'Número de Personas Atrapadas': Numero_Personas_Atrapadas,
'Número de Personas Desaparecidas': Numero_Personas_Desaparecidas,
'Número de Personas Fallecidas': Numero_Personas_Fallecidas,
'Número de Personas Lesionadas': Numero_Personas_Lesionadas,
'Número de Personas Rescatadas': Numero_Personas_Rescatadas,
'Otra Referencia de Ubicación ': Otra_Referencia_Ubicacion,
'Timestamp' : Timestamp,
'Tipo de Infraestructura': Tipo_Infraestructura,
'Tipo de Uso': Tipo_de_Uso,
'Tipo del Daño': Tipo_del_Danio,
'Verificado' : Verificado,
'Víveres Faltantes ': Viveres_Faltantes,
'Víveres Sobrantes ': Viveres_Sobrantes,
'latitud': latitud,
'longitud': longitud
	})

Har_Mit.drop(Har_Mit.index[0])

Har_Mit.to_csv('Harvard_MIT.csv')

