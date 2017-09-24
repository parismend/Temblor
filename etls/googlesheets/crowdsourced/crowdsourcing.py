"""
Este módulo maneja la autenticación con Google,
y lee e inserta datos en un Spreadsheet.
El archivo generado es datos.csv.
"""
# Correr desde HOME
import re
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pandas as pd
import os
import httplib2
from geopy.geocoders import GoogleV3
from Dicc_Tipo_Danhos import camb_tipos
import tqdm
import unidecode


print("Hola ETL")
print(os.getcwd())

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
        spreadsheetId='1MNdlW00Kr1A88Oq7gQOayIoIZrpX_krbKJlVc8e6O3c',
        range='Form Responses 1!A1:AC10000').execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        return values


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
    info = estructura_sheet(data)
    info_pub = info.drop([
        'Nombre del informante ',
        'Teléfono o correo del informante'],
        axis=1)

    info_pub.loc[info_pub.Consentimiento.str.contains('No acepto'),
                 'Teléfono del acopio/albergue'] = ''

    calles = info_pub['Calle'].tolist()
    numeros = info_pub['Número Exterior  o Aproximado (escribe sólo el número)'].tolist()
    munis = info_pub['Delegación o Municipio'].tolist()
    estados = info_pub['Estado'].tolist()

    for col in info_pub.columns:
        print(col)
        info_pub[col] = info_pub[col].apply(lambda x: unidecode.unidecode(x))

    # coordenadas
    lati = []
    longi = []
    for i in tqdm.tqdm(range(info_pub.shape[0])):
        lat_aux, lon_aux = obtain_latlong(dir_correct(
            calles[i], numeros[i], str(munis[i]), str(estados[i])))
        lati.append(lat_aux)
        longi.append(lon_aux)
    info_pub['latitud'] = lati
    info_pub['longitud'] = longi

    info_pub.columns = [re.sub('[<>{}\|]', '', x) for x in info_pub.columns]
    info_pub.columns = [re.sub('\(.*\)', '', x) for x in info_pub.columns]
    info_pub.columns = [x[0:60] for x in info_pub.columns]
    # Faltantes
    for col in info_pub.columns[info_pub.columns.str.contains('alta')]:
        info_pub.loc[
            info_pub[col] == '',
            col] = 'Si tienes info entra a: http://bit.ly/Verificado19s'
    for col in info_pub.columns[info_pub.columns.str.contains('obra')]:
        info_pub.loc[
            info_pub[col] == '',
            col] = 'Si tienes info entra a: http://bit.ly/Verificado19s'

    dicc_danios = camb_tipos()

    info_pub = info_pub.merge(pd.DataFrame({
        'Tipo de Daño ': list(dicc_danios.keys()),
        'Tipo Daño': list(dicc_danios.values())}))

    info_pub['Tipo del Daño'] = info_pub['Tipo Daño']
    info_pub.drop('Tipo Daño', axis=1)

    info_pub[info_pub.latitud != ''].to_csv('datos_crowdsourced.csv')
