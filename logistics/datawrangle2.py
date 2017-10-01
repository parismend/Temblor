# -*- coding: utf-8 -*-

# Por ahora, este código corre desde logistics
import googlemaps
import pandas as pd
import re
from unidecode import unidecode as uc
from datetime import datetime
from uglydicts2 import translate_dict

# Poner clave API Google Geocoding aquí:
gmaps = googlemaps.Client(key='')

""" Esta función abre y junta el nuevo csv con supply_demand.csv y descarta duplicados """
def clean(gsheets):
    new_df = pd.read_csv(gsheets, encoding='utf-8')
    new_df = new_df.rename(index=str, columns=translate_dict)
# Crear nuevas columnas en new_df
    new_df['loc_name'] = None
    new_df['loc_id'] = None
    new_df['lat_lng'] = None

# Abrir csv existente
    old_df = pd.read_csv('data/supply_demand.csv', encoding='utf-8')

# Concatenar csvs y descartar duplicados
    frames = [old_df, new_df]
    for i in range(len(frames)):
        frames[i].columns = [x.strip() for x in frames[i].columns]
    dup_v = ['loc_name', 'tstamp']
    df = pd.concat(frames).drop_duplicates(subset=dup_v, keep='first').reset_index(drop=True)
    return df


""" Función que agrega ID, Nombre, lat_lng a data frame """
# [ ] To do: mejorar nombres de centros y agregar UUID o alguna clave única simplificada
def g_geocode(x):
    geocode_result = gmaps.geocode(x)
    geocode_locdict = {}

# Si gmaps da un resultado, saca nombre de localización, código postal, latitud y longitud y los formatea
    if geocode_result != []:
        dict_name = uc(geocode_result[0]['address_components'][1]['short_name'])
        zip_code = uc(geocode_result[0]['address_components'][-1]['short_name'])
        geocode_locdict['name'] = re.sub('[^A-Za-z0-9]+', '',dict_name)[:7] +"-"+ zip_code
        latitud = geocode_result[0]['geometry']['location']['lat']
        longitud = geocode_result[0]['geometry']['location']['lng']
        geocode_locdict['lat_lng'] = format(latitud,'.3f'), format(longitud,'.3f')
    else:
        geocode_locdict = {'name': 'no encontrado', 'lat_lng': ('0', '0')} 
    print (geocode_locdict, ": \n", x)
    return (geocode_locdict)


# Inicializa el script y guarda como df, consolidated dataframe
if __name__ == '__main__':
    df = clean('data/query.csv')

# Junta municipios en una sola columna
    municipios = ['dir_mun_pue', 'dir_mun_chi', 'dir_mun_oax', 'dir_mun_gue', 'dir_mun_mor', 'dir_mun_otro']
    df[municipios] = df[municipios].astype(str)
    df['dir_mun'] = df.loc[df['dir_mun'].isnull(), municipios].apply(lambda x: "".join(x))

# Lista para concatenar en dirección ge búsqueda g_search_string
    lista = ['dir_calle', 'dir_loc', 'dir_mun', 'dir_est']
    df[lista] = df[lista].astype(str)

# Vector de filas donde no hay lat_lng
    search_v = df['lat_lng'].isnull()

# Concatena columnas en una dirección para API de gmaps
    df['g_search_string'] = df.loc[search_v, lista].apply(lambda x: ' '.join(x), axis = 1)

# Genera lat_lng y lo formatea a partir de g_search_string
    df['lat_lng'] = df.loc[df['lat_lng'].notnull(),'lat_lng'].apply(lambda x: ", ".join(x))
    df['lat_lng'] = df.loc[search_v,'g_search_string'].apply(lambda x: g_geocode(x)['lat_lng'])

# Guardar dataframe como "supply_demand.csv". Este es el nuevo old_df
    df.drop('g_search_string', axis=1)
    filename = 'data/supply_demand.csv'
    print('saving DF to csv:' + filename)
    df.to_csv(filename, index=False, encoding='utf-8')
    
