from abstract_mailer import Mailer
from mailjet_rest import Client
import json
import pickle
import os


class Mailjet(Mailer):
    def get_mails(self):
        users_data = []
        messages = self.api_client.message.get(filters={'Limit':50}).json()

        parsed_data = self.parse_data(messages)

        with open('mj_data', 'wb') as mj_data:
            pickle.dump(parsed_data, mj_data)
        with open('mj_data.json', 'w') as mj_data_json:
            json.dump(parsed_data, mj_data_json)

    # def get_id_of_wanted_address(self, mail_address):
    #     sender_filters = {'Email': mail_address}
    #     sender = self.api_client.sender.get(filters=sender_filters).json()['Data'][0]
    #     return sender['ID']

    def parse_data(self, raw_data):
        parsed_data = []
        for message in raw_data["Data"]:
            parsed_message = {
                'date': str(message['ArrivedAt']),
                'subject': message['Subject'],
                'sender': self.api_client.sender.get(id=message['SenderID']).json()['Data'][0]['Email'],
                'receiver': self.api_client.contact.get(id=message['ContactID']).json()['Data'][0]['Email'],
                'mailer': 'Mailjet',
                'state': message['Status'],
            }
            parsed_data.append(parsed_message)
        return parsed_data

    def __init__(self):
        api_key = os.environ['MJ_APIKEY_PUBLIC']
        api_secret = os.environ['MJ_APIKEY_PRIVATE']
        self.api_client = Client(auth=(api_key, api_secret), version='v3')