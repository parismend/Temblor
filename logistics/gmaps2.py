# -*- coding: utf-8 -*-
import googlemaps 
import pandas as pd
from datetime import datetime

# Poner clave API Google Geocoding aquí:
gmaps = googlemaps.Client(key='AIzaSyA29aEYe0FwdHKQ5YY0KRpFnPRbiSHOqf8')

def p_read(csv):
    df = pd.read_csv(csv)
    notnullv = df['dir_num'].notnull()

    df['dir_num'] = df.loc[notnullv, 'dir_num'].apply(lambda x: format(x,'.0f'))
    df['dir_estado'] = df['dir_estado'].astype(str)
    return df

# Obtiene y formatea coordenadas de gmaps
def g_geocode(x):
    geocode_result = gmaps.geocode(x)
    geocode_locdict = {}
    if geocode_result != []:        
        geocode_locdict['lat'] = format(geocode_result[0]['geometry']['location']['lat'],'.3f')
        geocode_locdict['lng'] = format(geocode_result[0]['geometry']['location']['lng'],'.3f')
    else:
        geocode_locdict = {'lat': '0', 'lng': '0'} 
    print ((geocode_locdict['lat'], geocode_locdict['lng']), ': ', x)
    return (geocode_locdict['lat'], geocode_locdict['lng'])

if __name__ == '__main__':
    df = p_read('data/logistics.csv')
    
    # Declarar listas
    lista = ['dir_calle', 'dir_num', 'dir_col', 'dir_del', 'dir_estado']
    droplist = ['g_search_string', 'lat', 'lng']
    has_coord = df['lat_lng'].notnull()
    has_address = df['dir_calle'].notnull() & df['dir_num'].notnull() & df['dir_col'].notnull() & df['dir_del'].notnull() & df['dir_del'] & df['dir_estado']
    is_valid = has_coord | has_address

    df['g_search_string'] = df.loc[is_valid, lista].apply(lambda x: ' '.join(x), axis = 1)
    df['lat_lng'] = df.loc[is_valid,'g_search_string'].apply(lambda x: g_geocode(x))
    df['lat_lng'] = df.loc[df['lat_lng'].notnull(),'lat_lng'].apply(lambda x: ", ".join(x))

    # Descartar columnas no utilizadas
    df.drop(droplist, axis=1)

    # Guardar a csv
    filename = 'data/logisticsgps.csv'
    df.to_csv(filename, index=False, encoding='utf-8')

