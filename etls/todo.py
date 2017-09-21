import luigi

class LimpiaGoogleSheets(luigi.Task):
    update_id = luigi.Parameter()
    google_spreedsheet = luigi.Parameter()
    google_secret = luigi.Parameter()
    query_date = luigi.Parameter()

    def run(self):
    	# print(self.google_secret,self.google_spreedsheet)
        with self.output().open('w') as output_file:
            output_file.write('Hola google')

    def output(self):
    	print ("tmp/corrida_{}.csv")
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