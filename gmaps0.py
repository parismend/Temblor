# -*- coding: utf-8 -*-
import googlemaps 
import pandas as pd
from datetime import datetime

gmaps = googlemaps.Client(key='')

def p_read(csv):
    df = pd.read_csv(csv)
    return df
    
if __name__ == '__main__':
    df = p_read('test.csv')    
    new_df = pd.DataFrame()

    for row in df.iterrows():
        if str(row[1][3]) != 'nan' or str(row[1][4]) != 'nan':
            if str(row[1][-2]) == 'nan':
                print('trying', row[1][-2])
                geocode_result = gmaps.geocode((str(row[1][3])+" "+str(row[1][4])+", "+str(row[1][5])+", "+str(row[1][6])))
                try:
                    row[1][-2] = geocode_result[0]['geometry']['location']['lat']
                    row[1][-1] = geocode_result[0]['geometry']['location']['lng']
                    print(row[1][-1], row[1][-2])
                except:
                    row[1][-2] = 'no encontrado'
                    row[1][-2] = 'no encontrado'
                    
    

