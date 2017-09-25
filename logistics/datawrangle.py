# -*- coding: utf-8 -*-
import pandas as pd
from unidecode import unidecode as uc
from datetime import datetime
from uglydicts import gsheets_bquery, bquery_clean, clean_list, check_list

# Esta función reemplaza valores encontrados en clean_list con None (borra datos sucios)
def p_replace(x):
    x = uc(str(x).lower())
    if x in clean_list:
        return clean_list[x]
    else:
        return x


# Esta función es la principa. Lee el gspreadsheet de Oferta/demanda y los datos exportados de BigQuery del back end
def clean(gsheets, bquery):
    df_gs = pd.read_csv(gsheets, encoding='utf-8')
    df_gs = df_gs.rename(index=str, columns=gsheets_bquery)

    df_bq = pd.read_csv(bquery, encoding='utf-8')

    frames = [df_gs, df_bq]

    for i in range(len(frames)):
        frames[i].columns = [x.strip() for x in frames[i].columns]

    df = pd.concat(frames).drop_duplicates().reset_index(drop=True)
    df = df.rename(index=str, columns=bquery_clean)

    #df.ix[:, check_list].apply(lambda x: p_replace(x), axis=1)

    return df


# Inicializa el script
if __name__ == '__main__':
    df = clean('data/acopiosheets.csv', 'data/acopioreqs.csv')

    for col in df.columns:
        df[col] = df[col].apply(lambda x: p_replace(x))
    
    print('saving DF to csv: logistics.csv')
    filename = 'data/logistics.csv'
    df.to_csv(filename, index=False, encoding='utf-8')
    

