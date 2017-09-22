# -*- coding: utf-8 -*-
import googlemaps 
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key='')

def p_read(csv):
    df = pd.read_csv(csv)
    # Convierte Número de calle en str para concatenar... no se ve bien pero funciona
    df['strnum'] = df['Número (aproximado al menos)'].map(str)
    return df

def g_geocode(x):
    x = x.max()
    geocode_result = gmaps.geocode(x)
    print(geocode_result)
    if geocode_result != []:
        geocode_locdict = geocode_result[0]['geometry']['location']
    else:
        geocode_locdict = {'lat': 'no encontrada', 'lng': 'no encontrada'}        
    return geocode_locdict

if __name__ == '__main__':
    df = p_read('test.csv')    
    is_valid = df['Calle'].notnull() & df['strnum'].notnull() & df['Colonia'].notnull() & df['Delegación o municipio'].notnull()
    is_missing = df['latitud'].isnull() & df['longitud'].isnull()
    apply_vector = is_valid & is_missing

    # No está regresando las coordenadas todavía pero g_geocode sí las encuentra...
    df['g_search_string'] = df.loc[apply_vector,["Calle", "strnum", "Colonia", "Delegación o municipio"]].apply(lambda x: ' '.join(x), axis = 1)
    df["latitud"] = df.loc[apply_vector,['g_search_string']].apply(lambda x: g_geocode(x)['lat'])
    df["longitud"] = df.loc[apply_vector,['g_search_string']].apply(lambda x: g_geocode(x)['lng'])
    df.drop('g_search_string', axis=1)

    print(df.loc[apply_vector])

