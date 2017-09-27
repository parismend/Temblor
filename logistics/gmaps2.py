# -*- coding: utf-8 -*-
import googlemaps
import pandas as pd
import re
from unidecode import unidecode as uc
from datetime import datetime


# Poner clave API Google Geocoding aquí:
gmaps = googlemaps.Client(key='')

def p_read(csv):
    df = pd.read_csv(csv)
    notnullv = df['dir_num'].notnull()

    df['dir_num'] = df.loc[notnullv, 'dir_num'].apply(lambda x: format(x,'.0f'))
    #df['dir_estado'] = df['dir_estado'].astype(str)
    return df

# Obtiene y formatea coordenadas de gmaps
def g_geocode(x):
    geocode_result = gmaps.geocode(x)
    geocode_locdict = {}
    if geocode_result != []:
        # To-do: mejorar legibilidad de claves. Quitar calle, av, etc)
        geocode_locdict['name'] = re.sub('[^A-Za-z0-9]+', '',uc(geocode_result[0]['address_components'][1]['short_name']))[:7] +"-"+ uc(geocode_result[0]['address_components'][-1]['short_name'])
        geocode_locdict['lat_lng'] = format(geocode_result[0]['geometry']['location']['lat'],'.3f'), format(geocode_result[0]['geometry']['location']['lng'],'.3f')
    else:
        geocode_locdict = {'name': 'no encontrado', 'lat_lng': ('0', '0')} 
    print (geocode_locdict, ": \n", x)
    return (geocode_locdict)

if __name__ == '__main__':
    df = p_read('data/logistics_needs.csv')
    
    # Declarar listas
    lista = ['dir_calle', 'dir_num', 'dir_col', 'dir_del', 'dir_estado']
    droplist = ['g_search_string', 'lat', 'lng']
    has_coord = df['lat_lng'].notnull()
    has_address = df['dir_calle'].notnull() & df['dir_num'].notnull() & df['dir_col'].notnull() & df['dir_del'].notnull() & df['dir_del'] & df['dir_estado']
    is_valid = has_coord | has_address

    df['g_search_string'] = df.loc[is_valid, lista].apply(lambda x: ' '.join(x), axis = 1)
    df['lat_lng'] = df.loc[is_valid,'g_search_string'].apply(lambda x: g_geocode(x)['lat_lng'])
    df['lat_lng'] = df.loc[df['lat_lng'].notnull(),'lat_lng'].apply(lambda x: ", ".join(x))

    # Descartar columnas no utilizadas
    df.drop(droplist, axis=1)

    # Guardar a csv
    filename = 'data/logisticsgps.csv'
    df.to_csv(filename, index=False, encoding='utf-8')

