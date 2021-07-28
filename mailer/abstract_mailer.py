from abc import ABC, abstractmethod


class Mailer:
    @abstractmethod
    def get_user_informations(self, address_list):
        pass

    @abstractmethod
    def parse_message(self, message_data):
        pass
