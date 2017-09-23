from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import httplib2
import argparse
import pandas as pd
import geopy as gp
from geopy.geocoders import GoogleV3
import numpy as np
from oauth2client.file import Storage
import logging
import tqdm
import csv
import re

try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'creds/secreto_cliente.json'
APPLICATION_NAME = 'Descargas'
geolocator = GoogleV3(api_key=os.environ.get('GM_KEY'))


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
        spreadsheetId='1Te3qe0BXvQiO8nNd5zemrYdEQjARaWeKRzwUm2XQwsI',
        range='Respuestas de formulario 1!A1:W1000').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values


# Dirección debe ser de la forma "Num Calle Ciudad"
def dir_correct(calle, numero, ciudad, estado):
    k = []
    k.append(calle + ' ' + numero)
    k.append(ciudad)
    k.append(estado + ', ' + 'MX')
    dirr = ', '.join(k)
    return dirr


def obtain_latlong(dirr):
    try:
        location = geolocator.geocode(dirr, region='MX')
        lat = location.latitude
        lon = location.longitude
    except:
        lat = ''
        lon = ''
    return lat, lon


def get_latlon(df):
    calle = df['Calle'].tolist()
    numero = df['Número (aproximado al menos)'].tolist()
    ciudad = df['Estado '].tolist()
    lati = []
    longi = []
    # dirr=dir_correct(calle, numero)
    # lat,lon = obtain_latlong(dirr)
    for i in range(df.shape[0]):
        try:
            lat_aux, lon_aux = obtain_latlong(
                dir_correct(calle[i], str(numero[i]), ciudad[i]))
        except:
            lat_aux = ''
            lon_aux = ''
        lati.append(lat_aux)
        longi.append(lon_aux)
        print(lat_aux, lon_aux)
    df['latitud'] = lati
    df['longitud'] = longi
    return df


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
    acopio = get_Data_temblor()
    acopio = estructura_sheet(acopio)
    calles = acopio['Calle'].tolist()
    numeros = acopio['Número (aproximado al menos)'].tolist()
    munis = acopio['Delegación o municipio'].tolist()
    estados = acopio['Estado '].tolist()
    # coordenadas
    lati = []
    longi = []
    for i in tqdm.tqdm(range(acopio.shape[0])):
        lat_aux, lon_aux = obtain_latlong(dir_correct(
            calles[i], numeros[i], str(munis[i]), str(estados[i])))
        lati.append(lat_aux)
        longi.append(lon_aux)
    acopio['latitud'] = lati
    acopio['longitud'] = longi
    acopio.columns = [re.sub('[ <>{}\|]', '', x) for x in acopio.columns]
    acopio.columns = [re.sub('\(.*\)', '', x) for x in acopio.columns]
    acopio.columns = [re.sub('[^A-Z^a-z]', '', x) for x in acopio.columns]
    for col in acopio.columns[acopio.columns.str.contains('altante')]:
        acopio[col] = acopio[col].apply(
            lambda x: re.sub('[^A-Z^a-z^ ]', '', str(x)))
    for col in acopio.columns[acopio.columns.str.contains('istente')]:
        acopio[col] = acopio[col].apply(
            lambda x: re.sub('[^A-Z^a-z^ ]', '', str(x)))
    acopio[acopio.latitud != ''].to_csv('acopio.csv', encoding='utf-8')
