from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pandas as pd
import os
import httplib2
from geopy.geocoders import Nominatim


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'creds/secreto_cliente.json'
APPLICATION_NAME = 'Temblor'
geolocator = Nominatim()


# Dirección debe ser de la forma "Num Calle Ciudad"
def dir_correct(calle, numero):
    k = []
    k.append(numero)
    k.append(calle)
    k.append('cdmx')
    dirr = ' '.join(k)

    return dirr


def obtain_latlong(dirr):
    try:
        location = geolocator.geocode(dirr)
        return (location.latitude, location.longitude)
    except:
        return ('', '')


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credetntial_path = os.environ.get('CREDENTIALS_PATH')
    credential_path = os.path.join(
        credetntial_path,
        'sheets.googleapis.com-python-quickstart.json'
    )

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


def get_data_temblor():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build(
        'sheets',
        'v4',
        http=http,
        discoveryServiceUrl=discoveryUrl
    )
    # DAÑOS Y DERRUMBES VERIFICADOS
    # Para descargar otras páginas cambiar el onmbre en el campo range
    result = service.spreadsheets().values().get(
        spreadsheetId='1CC5BqKv7Pqx5V2wtoJUNN7fOGOPtFyT5XOhSjfVhai8',
        range='Form Responses 1!A1:AH10000').execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values


def insert_data_temblor(datos):
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
        range='Datos!A1:H1500').execute()
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
