from utils.danio_lib import dir_correct,obtain_latlong,get_credentials,get_Data_temblor,insert_Data_temblor,estructura_sheet
import re

if __name__ == '__main__':
    data = get_Data_temblor()
    info = estructura_sheet(data)
    info_pub = info.drop([
        'Nombre del Informante (esta información no será pública)',
        'Teléfono de Contacto (esta información no será pública)'],
        axis=1)

    calles = info_pub['Calle'].tolist()
    numeros = info_pub['Número Exterior  o Aproximado (escribe sólo el número)'].tolist()
    lati = []
    longi = []
    for i in range(info_pub.shape[0]):
        lat_aux, lon_aux = obtain_latlong(dir_correct(
            calles[i], numeros[i]))
        lati.append(lat_aux)
        longi.append(lon_aux)
    info_pub.columns = [re.sub('[<>{}\|]', '', x) for x in info_pub.columns]
    info_pub.columns = [re.sub('\(.*\)', '', x) for x in info_pub.columns]
    info_pub.columns = [x[0:60] for x in info_pub.columns]
    info_pub['latitud'] = lati
    info_pub['longitud'] = longi
    info_pub.to_csv('datos.csv')
