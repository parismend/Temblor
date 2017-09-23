#-*- coding: utf-8 -*-

import os
import glob
import geocoder
import pandas as pd
import geopandas as gpd
from joblib import Parallel, delayed
from shapely.geometry import Point
# se tiene que instalar también libspatialindex y rtree


def concatenar_info_calle(calle, numero, colonia,
                          delegacion, estado):
    address = ', '.join([calle + ' ' + numero, colonia, delegacion, estado])
    address = address.replace('nan', '').replace('  ', ' ').strip()
    if address != ', , ,':
        return address
    else:
        return None


def geocode_google(calle, numero, colonia,
                   delegacion, estado, google_key):
    direccion = concatenar_info_calle(calle, numero, colonia, delegacion, estado)
    output = {}
    if direccion is not None:
        google_response = geocoder.google(direccion, key=google_key)
        if len(google_response.geojson['features']) == 0:
            return output
        resp = google_response.geojson['features'][0]
        confidence = resp['properties']['confidence']
        output['confidence'] = confidence
        coords = resp['geometry']['coordinates']
        output['google_lon'] = coords[0]
        output['google_lat'] = coords[1]
        # output['coords'] = coords
        address_components = resp['properties']['raw']['address_components']
        for element in address_components:
            if 'street_number' in element['types']:
                output['google_st_number'] = element['long_name']
            if 'route' in element['types']:
                output['google_calle'] = element['long_name']
            if 'sublocality' in element['types']:
                output['google_colonia'] = element['long_name']
            if 'administrative_area_level_1' in element['types']:
                output['google_estado'] = element['long_name']
        return output
    return output


def make_google_request(row, google_key):
    calle = str(row.Calle)
    numero = str(row.NmeroExterioroAproximado)
    if numero.startswith('0'):
        numero = 'nan'
    colonia = str(row.Colonia)
    delegacion = str(row.Delegacin)
    estado = str(row.Estado)
    address = concatenar_info_calle(calle, numero, colonia, delegacion, estado)
    if address is not None:
        google_response = geocoder.google(address, key=google_key)
        if len(google_response.geojson['features']) == 0:
            return None
        resp = google_response.geojson['features'][0]
        confidence = resp['properties']['confidence']
        row['google_confidence'] = confidence
        a_components = resp['properties']['raw']['address_components']

        for e in a_components:
            if 'street_number' in e['types']:
                row['google_st_number'] = e['long_name']
            if 'route' in e['types']:
                row['google_calle'] = e['long_name']
            if 'sublocality' in e['types']:
                row['google_colonia'] = e['long_name']
            if 'administrative_area_level_1' in e['types']:
                row['google_estado'] = e['long_name']
        coords = resp['geometry']['coordinates']
        row['google_lat'], row['google_lon'] = coords[1], coords[0]
        new_row = pd.DataFrame(row).T
        return new_row
    return None


if __name__ == '__main__':
    google_key = os.environ.get('GM_KEY')
    path_danios = os.environ.get('PATH_DANIOS')
    # ALGO ASI '../../../datos/manzanas_inegi/man*.shp'
    path_manzanas = os.environ.get('PATH_MANZANAS')

    # path_save_danios = os.environ.get('PATH_DANIOS_SAVE')
    df_danios = pd.read_csv(
        path_danios, parse_dates=['Timestamp'],
        dtype={
            'Calle': str, 'Colonia': str, 'Delegacin': str, 'Estado': str,
            'NmeroExterioroAproximado': str
        }
    )
    radius_buffer = 0.0001
    # df_danios = df_danios.assign(
    #     numero_exterior=df_danios['Número Exterior  o Aproximado'],
    #     Delegacion=df_danios['Delegación'],
    # )
    df_danios = df_danios.assign(fuente='')
    df_danios.loc[df_danios.Calle.isnull(), 'fuente'] = 'JSON'
    df_danios.loc[df_danios.Calle.isnull(), 'fuente'] = 'georref'

    # Call google
    print('Geocoding ...')
    google_key = os.environ.get('GOOGLE_API_KEY')
    # Sequential requests
    # df_google_danios = []
    # for _, row in df_danios.iterrows():
    #     respuesta = make_google_request(row, google_key)
    #     df_google_danios.append(respuesta)

    # Concurrent requests
    df_google_danios = Parallel(n_jobs=-1, backend="threading")(
        delayed(make_google_request)(row, google_key) for i, row in df_danios.iterrows()
    )
    df_google_danios = pd.concat(
        [row for row in df_google_danios if row is not None], ignore_index=True, axis=0
    )
    df_google_danios = df_google_danios[
        df_google_danios.google_estado.isin(['Ciudad de México', 'Morelos', 'Puebla'])
    ]
    df_google_danios = df_google_danios.assign(
        google_calle=df_google_danios.google_calle.fillna(df_google_danios.Calle)
    )

    df_google_danios = df_google_danios.loc[df_google_danios.google_confidence >= 8]

    # Geo-ref
    print('Loading cvegeos...')
    files = [file for file in glob.glob(path_manzanas)]
    df_mnz = Parallel(n_jobs=-1)(delayed(gpd.read_file)(file) for file in files)
    df_mnz = pd.concat(df_mnz, axis=0, ignore_index=True)
    df_mnz = df_mnz.to_crs({'init': 'epsg:4326'})

    aux = df_danios.loc[df_danios.fuente == 'JSON']
    aux = aux.assign(lat=aux.latitud, lon=aux.longitud)

    aux2 = df_google_danios.rename(
        columns={'google_lat': 'lat', 'google_lon': 'lon'})

    aux = pd.concat([aux2, aux], ignore_index=True, axis=0)

    geometry = [Point(xy) for xy in zip(aux.lon, aux.lat)]

    crs = {'init': 'epsg:4326'}
    geo_df = gpd.GeoDataFrame(aux, crs=crs, geometry=geometry)
    geo_df['geometry'] = geo_df.geometry.buffer(radius_buffer)
    geo_df = geo_df.to_crs({'init': 'epsg:4326'})
    print('Spatial joint between points and manzanas ...')
    danios_manzana = gpd.sjoin(geo_df, df_mnz, how="inner", op='intersects')

    danios_manzana = danios_manzana.sort_values('Timestamp', ascending=False)
    danios_manzana.to_csv('danios_zonas.csv', index=False)
    limpio_danios = danios_manzana.reset_index().drop_duplicates(subset='index')
    limpio_danios = limpio_danios.drop_duplicates(subset='cvegeo')
    limpio_danios = limpio_danios.drop(
        ['geometry', 'index_right', 'tipomza', 'latitud', 'longitud'],
        axis=1
    )
    limpio_danios = limpio_danios.rename(
        columns={'lat': 'latitud', 'lon': 'longitud'})
    limpio_danios = pd.DataFrame(limpio_danios)
    final_cols = [
        'Calle', 'Colonia', 'Delegacin', 'EspecialistasFaltantesseparaporcomas', 'Estado', 'Foto',
        'HerramientasExistentes', 'HerramientasFaltantes', 'Hora', 'HoradelReporte',
        'ManodeObraExistente', 'ManodeObraFaltante', 'MedicamentosExistentes',
        'MedicamentosFaltantes', 'Municipio', 'NmeroExterioroAproximado',
        'NmerodePersonasAtrapadas', 'NmerodePersonasDesaparecidas', 'NmerodePersonasFallecidas',
        'NmerodePersonasLesionadas', 'NmerodePersonasRescatadas', 'OtraReferenciadeUbicacin',
        'Timestamp', 'TipoDao', 'TipodeInfraestructura', 'TipodeUso', 'TipodelDao', 'Verificado',
        'VveresExistentes', 'VveresFaltantes', 'VveresSobrantes', 'latitud', 'longitud'
    ]
    limpio_danios = limpio_danios.loc[:, final_cols]
    print('Writing output')
    limpio_danios.to_csv(
        'danios_clean.csv', index=False, quoting=1, encoding='utf-8'
    )
