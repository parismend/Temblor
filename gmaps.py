# -*- coding: utf-8 -*-
import googlemaps 
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key='')

def p_read(csv):
    df = pd.read_csv(csv)
    return df

def g_geocode(calle, numero, colonia, delegacion):
    geocode_result = gmaps.geocode((str(calle)+" "+str(numero)+", "+str(colonia)+", "+str(delegacion)))
    geocode_locdict = geocode_result[0]['geometry']['location']
    return geocode_locdict

if __name__ == '__main__':
    df = p_read('test.csv')    
    is_valid = df['Calle'].notnull() | df['Colonia'].notnull()
    is_missing = df['latitud'].isnull() | df['longitud'].isnull()
    apply_vector = is_valid * is_missing

    # Falta vsacar los varios argumentos o volver en un string
    df[apply_vector]['latitud'] = df.loc[apply_vector,["Calle", "Número", "Colonia", "Delegación o municipio"]].apply(lambda x: print(x))
