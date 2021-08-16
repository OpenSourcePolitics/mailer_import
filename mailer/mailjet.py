from abstract_mailer import Mailer
from mailjet_rest import Client
from datetime import datetime
import json
import pandas as pd
import os

MAX_LEN_API_RESPONSE = 1000


class Mailjet(Mailer):
    def get_mails(self, senders):
        raw_data = []
        senders_id = self.get_id_of_senders(senders)
        for sender_id in senders_id:
            raw_data += self.get_mailjet_data(
                'message',
                additional_filters={'SenderID': sender_id}
            )

        parsed_data = self.parse_mails(raw_data)

        return parsed_data

    def get_id_of_senders(self, senders_mail):
        senders_data = self.get_mailjet_data('sender')
        wanted_senders = list(
            filter(lambda x: x['Email'] in senders_mail, senders_data)
        )
        return list(map(lambda x: x['ID'], wanted_senders))

    def parse_mails(self, raw_data):
        raw_data_df = pd.DataFrame(raw_data).rename(
            columns={'ID': 'ID_Message', 'Status': 'MessageStatus'}
        )
        sender_df = pd.DataFrame(self.get_mailjet_data('sender')).rename(
            columns={'ID': 'SenderID'}
        )
        contact_df = pd.DataFrame(self.get_mailjet_data('contact')).rename(
            columns={'ID': 'ContactID'}
        )

        merged_with_senders = pd.merge(
            raw_data_df,
            sender_df,
            on="SenderID"
        ).rename(columns={'Email': 'SenderEmail'})
        merged_with_contacts = pd.merge(
            merged_with_senders,
            contact_df,
            on="ContactID"
        ).rename(columns={'Email': 'ContactEmail'})

        parsed_data = merged_with_contacts.loc[
            :,
            ['ArrivedAt', 'Subject', 'SenderEmail', 'ContactEmail', 'MessageStatus']
        ]
        parsed_data['ArrivedAt'].transform(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ"))
        return parsed_data

    def get_mailjet_data(self, endpoint, additional_filters={}):
        file_path = f"{endpoint}_data.json"
        offset, limit = 0, 1000
        filters = {'Limit': limit, 'Offset': offset}
        data = []

        if not getattr(self.api_client, endpoint):
            raise NotImplementedError('Pass a correct for the Mailjet API')

        elif additional_filters.get('FromTS'):
            with open(file_path, 'r') as data_file:
                data = json.load(data_file)
            filters = additional_filters

        elif os.path.exists(file_path):
            with open(file_path, 'r') as data_file:
                return json.load(data_file)

        while True:
            print(offset)
            filters.update(additional_filters)
            request_data = getattr(self.api_client, endpoint).get(
                filters=filters
            ).json()
            data += request_data['Data']
            if request_data['Count'] != limit:
                break
            offset += limit
        data['Current date'] = round(datetime.now().timestamp())
        with open(file_path, 'w') as data_file:
            json.dump(data, data_file)
        return data

    def update_mailjet_data(self, endpoint, additional_filters={}):
        file_path = f"{endpoint}_data.json"

        with open(file_path, 'r') as data_file:
            data = json.load(data_file)

        last_update = data["Current Date"]
        
        return self.get_mailjet_data({'FromTS': last_update})

    def __init__(self):
        api_key = os.environ['MJ_APIKEY_PUBLIC']
        api_secret = os.environ['MJ_APIKEY_PRIVATE']
        self.api_client = Client(auth=(api_key, api_secret), version='v3')
