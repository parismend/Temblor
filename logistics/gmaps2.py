# -*- coding: utf-8 -*-
import googlemaps 
import pandas as pd
from datetime import datetime

# Poner clave API Google Geocoding aquí:
gmaps = googlemaps.Client(key='AIzaSyBWwIZv0T8ygPJdx0mZ4Iv6b3YchHqkbFw')

def p_read(csv):
    df = pd.read_csv(csv)
    # Convierte Número de calle en str para concatenar... no se ve bien, pero funciona
    not_null = df['dir_num'].notnull()
    df['dir_num'] = df.loc[not_null,'dir_num'].map(str)
    df['dir_estado'] = df['dir_estado'].map(str)
    return df

# Código está haciendo doble llamada a la API, pero sirve
def g_geocode(x):
    geocode_result = gmaps.geocode(x)
    if geocode_result != []:        
        geocode_locdict = geocode_result[0]['geometry']['location']
    else:
        geocode_locdict = {'lat': 0, 'lng': 0} 
    print(x, 'resultado: ', float(str(geocode_locdict['lat'])[:6]), float(str(geocode_locdict['lng'])[:7]))
    return (float(str(geocode_locdict['lat'])[:7]), float(str(geocode_locdict['lng'])[:8]))

if __name__ == '__main__':
    df = p_read('data/logistics.csv')
    is_valid = df['dir_calle'].notnull() & df['dir_col'].notnull() & df['dir_del'].notnull()
    lista = ['dir_calle', 'dir_num', 'dir_col', 'dir_del', 'dir_estado']
    df['g_search_string'] = df.loc[is_valid,lista].apply(lambda x: ' '.join(x), axis = 1)
    df['lat_lng'] = df.loc[is_valid,'g_search_string'].apply(lambda x: g_geocode(x))

    df.drop('g_search_string', axis=1)

    # Guardar a csv
    filename = 'data/logisticsgps.csv'
    df.to_csv(filename, index=False, encoding='utf-8')

