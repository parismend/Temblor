# Correr desde HOME
import re
import time
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pandas as pd
import os
import httplib2
from geopy.geocoders import GoogleV3
import tqdm

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
geolocator = GoogleV3(api_key=os.environ.get('GM_KEY'))


# Dirección debe ser de la forma "Num Calle Ciudad"
def dir_correct(calle, numero, ciudad, estado):
    k = []
    k.append('Calle ' + calle + ' ' + numero)
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
        spreadsheetId='1iZWfqPskSZkp35NRb-6vaxoZY6ErQ5LP77pqzlUjX5Y',
        range='Form Responses 1!A1:AH10000').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values


def estructura_sheet(listas):
    columnas = listas[0]
    del listas[0]
    info = pd.DataFrame()
    for lista in listas:
        dicc_aux = {}
        for col in range(len(lista)):
            dicc_aux[columnas[col]] = lista[col]
        info = info.append(dicc_aux, ignore_index=True)
    return info


if __name__ == '__main__':
    data = get_Data_temblor()
    info = estructura_sheet(data)
    info_pub = info.drop([
        'Nombre del contacto (esta información no se ha pública)',
        'Teléfono (esta información no se hará pública)'],
        axis=1)

    calles = info_pub['Calle'].tolist()
    numeros = info_pub['Número o Aproximado'].tolist()
    munis = info_pub['Delegación o municipio'].tolist()
    estados = info_pub['Estado'].tolist()
    lati = []
    longi = []
    print('Punteando...')
    for i in tqdm.tqdm(range(info_pub.shape[0])):
        lat_aux, lon_aux = obtain_latlong(dir_correct(
            calles[i], numeros[i], str(munis[i]), str(estados[i])))
        lati.append(lat_aux)
        longi.append(lon_aux)
    info_pub.columns = [re.sub('[<>{}\|]', '', x) for x in info_pub.columns]
    info_pub.columns = [re.sub('\(.*\)', '', x) for x in info_pub.columns]
    info_pub.columns = [x[0:60] for x in info_pub.columns]
    info_pub['latitud'] = lati
    info_pub['longitud'] = longi
    info_pub['Hora'] = time.time()
    info_pub.columns = [re.sub('[^A-Z^a-z]', '', x) for x in info_pub.columns]
    info_pub[info_pub.latitud != ''].to_csv('albergues.csv')
    info_pub[info_pub.latitud == ''].to_csv('albergues_sin_geo.csv')
