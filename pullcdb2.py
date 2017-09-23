import re
import math
import time
import pandas as pd
import urllib.request, json, datetime


def descarga_pandas(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        df = pd.DataFrame()
        for dictionary in data['rows']:
            df = df.append(dictionary, ignore_index=True)
        return df


def distancia(lat1, lon1, lat2, lon2):
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) * \
        math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d


if __name__ == '__main__':
    descifra = False
    crowdsource = False
    if descifra:
        ayuda_nec_link = 'https://descifra-admin.carto.com/api/v2/sql?q=select%20*%20from%20%22descifra-admin%22.ayudanecesitada'
        ayuda_vol_link = 'https://descifra-admin.carto.com/api/v2/sql?q=select%20*%20from%20%22descifra-admin%22.ayudavoluntaria'
        droplist = ['cartodb_id',
                    'contacto',
                    'estatus',
                    'the_geom',
                    'the_geom_webmercator',
                    'latlong']

        # REQUERIDA
        # Descargar df ayuda requerida y cambiar nombres
        df_nec = descarga_pandas(ayuda_nec_link)
        df_nec = df_nec.rename(index=str,
                               columns={"fechaalta": "Timestamp",
                                        "descripcion": "Víveres Faltantes"})

        # Filtrar columnas null y separar latlong en latitud y longitud
        df_nec = df_nec[df_nec.latlong.notnull()]
        latlong = [re.sub('\)', '', re.sub('POINT\(', '', str(x))).split()
                   for x in df_nec.latlong.tolist()]
        df_nec['latitud'] = [x[1] for x in latlong]
        df_nec['longitud'] = [x[0] for x in latlong]

        # Tirar columnas no requeridas y convertir datetime
        df_nec = df_nec.drop(droplist, axis=1)
        df_nec['Timestamp'] = df_nec['Timestamp'].apply(
            lambda x: datetime.datetime.strptime(x,
                '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y %H:%M:%S'))


        # OFRECIDA
        # Descargar df ayuda ofrecida y cambiar nombres
        df_vol = descarga_pandas(ayuda_vol_link)
        df_vol = df_vol.rename(index=str, columns={
            "latlon": "latlong",
            "fechaalta": "Timestamp",
            "descripcion": "Víveres Sobrantes"})

        # Filtrar columnas null y separar latlong en latitud y longitud
        df_vol = df_vol[df_vol.latlong.notnull()]
        latlong = [re.sub('\)', '', re.sub('POINT\(', '', str(x))).split()
                   for x in df_vol.latlong.tolist()]
        df_vol['latitud'] = [x[1] for x in latlong]
        df_vol['longitud'] = [x[0] for x in latlong]

        # Tirar columnas no requeridas y convertir datetime
        df_vol = df_vol.drop(droplist, axis=1)
        df_vol['Timestamp'] = df_vol['Timestamp'].apply(
            lambda x: datetime.datetime.strptime(
                x, '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y %H:%M:%S'))

    # FORMS
    # Abrir el CSV
    bs_csv = pd.read_csv('bici_squad.csv', header=0)
    bs_csv = bs_csv.drop(['Unnamed: 0'], axis=1)
    bs_csv['Foto'] = ''
    bs_csv['Hora'] = time.time()

    # Concatenar
    if descifra:
        if crowdsource:
            df_csv = pd.read_csv('datos.csv', header=0, skiprows=[1, 1])
            df_csv = df_csv.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
            frames = [df_nec, df_vol, df_csv, bs_csv]
        else:
            frames = [df_nec, df_vol, bs_csv]
    else:
        if crowdsource:
            df_csv = pd.read_csv('datos.csv', header=0, skiprows=[1, 1])
            df_csv = df_csv.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1)
            frames = [df_csv, bs_csv]
        else:
            frames = [bs_csv]

    for i in range(len(frames)):
        frames[i].columns = [x.strip() for x in frames[i].columns]

    danios = pd.concat(frames)

    # Info adicional
    for col in danios.columns[danios.columns.str.contains('alta')]:
#        danios.loc[danios[col] == '',
#                   col] = 'Si tienes info entra a: http://bit.ly/Verificado19s'
        danios.loc[danios[col].isnull(),
                   col] = 'Si tienes info entra a: http://bit.ly/Verificado19s'
    for col in danios.columns[danios.columns.str.contains('obra')]:
#        danios.loc[danios[col] == '',
#                   col] = 'Si tienes info entra a: http://bit.ly/Verificado19s'
        danios.loc[danios[col].isnull(),
                   col] = 'Si tienes info entra a: http://bit.ly/Verificado19s'

    # Guardar a csv
    filename = 'danios.csv'
    danios.columns = [re.sub('[^A-Z^a-z]', '', x) for x in danios.columns]
    danios = danios[~danios.latitud.isnull()]
    dist = []
    for i, row in danios.iterrows():
        dist.append(distancia(float(row.latitud), float(row.longitud),
                              19.3730816, -99.1374631))
    danios['dist'] = dist
    (danios[danios.dist < 300].drop('dist', axis=1).
        to_csv(filename, index=False, encoding='utf-8'))
