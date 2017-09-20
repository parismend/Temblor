import luigi

class LimpiaGoogleSheets(luigi.Task):
    update_id = luigi.Parameter()
    google_spreedsheet = luigi.Parameter()
    google_secret = luigi.Parameter()
    query_date = luigi.Parameter()

    def run(self):
    	
    	print(self.google_secret,self.google_spreedsheet)

    def output(self):
    	return luigi.LocalTarget("tmp/corrida_%s.csv" % self.query_date)


class RunAll(luigi.Task):
    def requires(self):
        params = {
            "google_spreedsheet":"asdf",
            "google_secret":"asdfdddd",
            "update_id":"124",
            "query_date":"134567"
        }
        return LimpiaGoogleSheets(**params)