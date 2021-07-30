import pandas as pd
import sib_api_v3_sdk as sib
from datetime import datetime, date, timedelta
import pickle
import sqlalchemy
from abstract_mailer import Mailer
import os
import json

class Sendinblue(Mailer):
    def get_mails(self, senders):
        api_instance = sib.TransactionalEmailsApi(self.api_client)
        data = api_instance.get_email_event_report(
            start_date = date.today() - timedelta(days=7),
            end_date = date.today(),
        ).to_dict()['events']
        data = list(filter(lambda x: x['_from'] in senders, data))
        parsed_data = self.parse_data(data)
        with open('sib_data', 'wb') as sib_data:
            pickle.dump(data, sib_data)
        with open('sib_data.json', 'w') as sib_data_json:
            json.dump(parsed_data, sib_data_json)

    def parse_data(self, data):
        parsed_data = []
        for event in data:
            parsed_event = {
                'date': str(event['_date']),
                'subject': event['subject'],
                'sender': event['_from'],
                'receiver': event['email'],
                'mailer': 'Sendinblue',
                'state': event['event'],
            }
            parsed_data.append(parsed_event)
        return parsed_data

    def __init__(self):
        configuration = sib.Configuration()
        configuration.api_key['api-key'] = os.environ['SIB_API_KEY']
        self.api_client = sib.ApiClient(configuration)