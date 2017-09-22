# -*- coding: utf-8 -*-
import googlemaps
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key='')

# Geocoding an address
def p_read(csv):
    df = pd.read_csv(csv, encoding="utf-8")
    df.reset_index()
    #df = df.drop('Column1', axis=1)
    return df

def geocodel(x):
    try: 
        geocode_result = gmaps.geocode_result(df['Calle'][x]+' '+df['Número'][x]+', '+df['Colonia'][x]+', '+df['Delegación'][x])
        dic = geocode_result[0]['geometry']['location']
    except:
        dic = {'lat': 'no encontrado', 'lng': 'no encontrado'}    
    return dic


if __name__ == '__main__':
    df = p_read('test.csv')
    df = df[df.Calle.notnull()]
    # cómo iterar bien aquí?
    if ['Calle'][x] != 0 and df['Colonia'][x] != 0:
        df['latitud'] = df['latitud'].apply(lambda x: geocodel(x)['lat'])
        df['longitud'] = df['longitud'].apply(lambda x: geocodel(x)['lng'])
        print(df['longitd'][x])

"""
df['Calle'] = [x[1] for x in Calle]
df['Timestamp'] = df['Timestamp'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y %H:%M:%S'))
"""    