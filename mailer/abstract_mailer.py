from abc import ABC, abstractmethod


class Mailer:
    @abstractmethod
    def get_mails(self, senders):
        pass

    @abstractmethod
    def parse_mails(self, mails):
        pass
