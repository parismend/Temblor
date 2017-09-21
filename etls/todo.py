import luigi
import re
from utils.danio_lib import dir_correct,obtain_latlong,get_credentials,get_Data_temblor,insert_Data_temblor,estructura_sheet
from sengrid_handler import _send_error


@luigi.Task.event_handler(luigi.Event.FAILURE)
def sendgrid_handler(task, exception=None):
    _send_error(task, exception)


class LimpiaGoogleSheets(luigi.Task):
    update_id = luigi.Parameter()
    google_spreedsheet = luigi.Parameter()
    google_secret = luigi.Parameter()
    query_date = luigi.Parameter()

    def run(self):
        # NOTA: Descomentar para probar el envio de mails
        # self.truena()

        with self.output().open('w') as output_file:
            output_file.write('Hola google')

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
        info_pub.to_csv("tmp/corrida_{}.csv".format(self.query_date))


    def output(self):
        # print ("tmp/corrida_{}.csv".format(self.query_date))
        return luigi.LocalTarget("tmp/corrida_{}.csv".format(self.query_date))


class RunAll(luigi.Task):
    def requires(self):
        params = {
            "google_spreedsheet":"asdf",
            "google_secret":"asdfdddd",
            "update_id":"124",
            "query_date":"134567"
        }
        return LimpiaGoogleSheets(**params)

    def output(self):
        return luigi.LocalTarget("tmp/_END")