from abstract_mailer import Mailer
from mailjet_rest import Client
import json
import pickle
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

        with open('parsed_message_data.json', 'w') as message_file:
            json.dump(parsed_data, message_file)

    def get_id_of_senders(self, senders_mail):
        senders_ids = []
        senders_data = self.get_mailjet_data('sender')
        wanted_senders = list(filter(lambda x: x['Email'] in senders_mail, senders_data))
        return list(map(lambda x: x['ID'], wanted_senders))

    def parse_mails(self, raw_data):
        parsed_data = []
        for message in raw_data:
            parsed_message = {
                'date': str(message['ArrivedAt']),
                'subject': message['Subject'],
                'sender': self.get_element_by_id('sender', message['SenderID'], 'ID'),
                'receiver': self.get_element_by_id('contact',message['ContactID'], 'ID'),
                'mailer': 'Mailjet',
                'state': message['Status'],
            }
            parsed_data.append(parsed_message)
        return parsed_data

    def get_mailjet_data(self, endpoint, additional_filters={}):
        file_path = f"{endpoint}_data.json"

        if not getattr(self.api_client, endpoint):
            raise NotImplementedError('Pass a correct for the Mailjet API')

        if os.path.exists(file_path):
            with open(file_path, 'r') as data_file:
                return json.load(data_file)

        offset = 0
        limit = 1000
        data = []
        while True:
            print(offset)
            filters = {'Limit':limit, 'Offset':offset}
            filters.update(additional_filters)
            request_data = getattr(self.api_client, endpoint).get(
                filters=filters
            ).json()
            data += request_data['Data']
            if request_data['Count'] != limit:
                break
            offset += limit
        with open(file_path, 'w') as data_file:
            json.dump(data,data_file)
        return data

    def get_element_by_id(self, endpoint, id, attr="ID"):
        data = self.get_mailjet_data(endpoint)
        return list(filter(lambda x: x[attr] == id, data))[0]['Email']

    def __init__(self):
        api_key = os.environ['MJ_APIKEY_PUBLIC']
        api_secret = os.environ['MJ_APIKEY_PRIVATE']
        self.api_client = Client(auth=(api_key, api_secret), version='v3')
