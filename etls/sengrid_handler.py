import os
import requests
import datetime


def _send_error(task, exception):
    response = requests.post(
        "https://api.mailgun.net/v3/sandbox82ec51efe6ff46d8aef7968f9eb56af7.mailgun.org/messages",
        auth=("api", os.environ.get('MAILGUN_API_KEY', 'key-83c82733faa51a845a1428ee5e67d2a3')),
        data={
            "from": "ETL TEMBLOR <postmaster@sandbox82ec51efe6ff46d8aef7968f9eb56af7.mailgun.org>",
            "to": os.environ.get('EMAIL_DESTINATION', "ETL BOX <{}>".format(os.environ.get('ETL_BOX_EMAIL', 'francisco@opianalytics.com'))),
            "subject": "ERROR DURANTE EL ETL {}".format(datetime.datetime.now().strftime("%Y/%m/%d")),
            "text": "Task: \n {} \nError: \n {}".format(str(task), str(exception))
        })

    print(response.json())


def sendgrid_handler(task, exception):
    _send_error(task, exception)
