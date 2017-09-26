# -*- coding: utf-8 -*-

# Por ahora, este código corre desde logistics
import pandas as pd
import re
import string
from unidecode import unidecode as uc
from datetime import datetime
from uglydicts import gsheets_bquery, bquery_clean, clean_list, check_list

# Esta función reemplaza valores encontrados en nuestros diccionarios con su valor estandarizado
# Si la primera palabra del artículo está en nuestro fw_dict, 
# se estandariza la primera palabra y se devuelven detalles adicionales
# Si la expresión completa está en clean_list, se estandariza la expresión completa. 
def p_replace(x):
    x = uc(str(x).lower())
    quant = re.search('^[0-9]+ ', x)
    quant_col = quant.group(0) if quant else ''
    x_item = re.sub('^[0-9]+ ', '', x)

    if x_item in clean_list:
        item_col = clean_list[x_item]
        details_col = ''
    else:
        split = re.split('\W+', x_item, 1)
        first_word = split[0]
        item_col = fw_dict[first_word] if first_word in fw_dict else x_item
        details_col = '' if len(split)==1 or first_word in fw_dict else split[1]

    return(quant_col, item_col, details_col)



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
    return df


# Inicializa el script
if __name__ == '__main__':
    df = clean('data/acopiosheets.csv', 'data/acopioreqs.csv')

    # Importamos nombres limpios para la primera palabra 
    fw = pd.read_csv('data/clean_names.csv')
    fw_dict = pd.Series(fw.clean_name.values, index = fw.name).to_dict()

    print('Registrando entradas')

    needs_data = pd.DataFrame(columns=['lat_long', 'pregunta', 'necesitan', \
        'cantidad', 'art', 'detalles'])

    for col in check_list:
        print(col)
        col_list = []
        necesitan = int(col.endswith('_f'))
        # Wishlist:
        # Quitar 'les faltan/les sobran/no tenemos/no hay/necesitamos/pedimos/se requieren/urgente'
        # Separar los casos con 'y'
        for row in range(0, len(df[col])):
            item_list = re.split(',', str(df[col][row]))
            for i in item_list:
                x = re.sub(r'[^\w\s]', '', i.strip('., '))
                quant,item,details = p_replace(x)
                col_list.append([df['lat_long'][row], col, necesitan, quant, item, details])
        needs_data = needs_data.append(pd.DataFrame(col_list, columns = needs_data.columns))

    filename = 'data/logistics_needs.csv'
    print('saving DF to csv:' + filename)
    df.to_csv(filename, index=False, encoding='utf-8')
    
