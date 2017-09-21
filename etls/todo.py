import luigi
# from googlesheets.limpia_etl.googlesheets import get_Data_temblor
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
        self.truena()

        with self.output().open('w') as output_file:
            output_file.write('Hola google')

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

luigi.run()