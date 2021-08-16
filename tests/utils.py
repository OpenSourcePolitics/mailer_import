import pytest
import json
import os
import mailer.main as main
from mailer.mailjet import Mailjet

FILE_NAME = 'dummy_emails.json'
emails_for_test = {
    'email': 'dummy_mail1@test.com',
    'email': 'dummy_mail2@test.com'
}

DATA_MAILJET = {
    'MJ_APIKEY_PUBLIC': 'dummy_PK',
    'MJ_APIKEY_PRIVATE': 'dummyPK'
}

DUMMY_MAILJET_ANSWER = {
    'Count': 10,
    'Data': [
        {
            'ArrivedAt': '2021-01-22T15:37:42Z',
            'AttachmentCount': 0,
            'AttemptCount': 0,
            'ContactAlt': '',
            'ContactID': 75179748,
            'Delay': 0,
            'DestinationID': 2,
            'FilterTime': 0,
            'ID': 93449692797113631,
            'IsClickTracked': True,
            'IsHTMLPartIncluded': False,
            'IsOpenTracked': True,
            'IsTextPartIncluded': False,
            'IsUnsubTracked': False,
            'MessageSize': 26930,
            'SenderID': 7525,
            'SpamassassinScore': 0,
            'SpamassRules': '',
            'StatePermanent': False,
            'Status': 'sent',
            'Subject': '',
            'UUID': 'a6063c95-1236-410b-89ec-b9469995cea7'
        }
    ]
}


DUMMY_SENDINBLUE_ANSWER = {
    None
}


@pytest.fixture(scope="module", autouse=True)
def emails_file_setup():
    with open(FILE_NAME, 'w') as f:
        json.dump(emails_for_test, f)

    yield

    os.remove(FILE_NAME)



class DummyMailerWorking:
    def __init__(self, mailer):
        if mailer == 'Mailjet'
        self.ok = True
        self.status_
    
    class message:
        def get(self):
            self.ok = True
            self.response_status = 200


@pytest.fixture
def good_mailjet_settings(monkeypatch):
    monkeypatch.settatr(main.mailjet, 'Mailjet', dummy_mailjet_working)



@pytest.fixture(scope="function", autouse=True)
def settings_init():
    settings.init(FILE_NAME, rdv_for_tests)


class DummyResponse:
    data = None

    def __init__(self, data):
        self.data = data.encode('utf-8')


def dummy_correct_http_get(method, url):
    return DummyResponse(
        '[{"dummy_data":"value"}]'
    )


def dummy_correct_http_get_subtabled(method, url):
    return DummyResponse(
        """[
            {
                "label": "Direct Entry"
            },
            {
                "label": "Websites",
                "subtable": [
                    {
                        "label": "sublabel"
                    }
                ]
            }
        ]"""
    )


def dummy_wrong_url_http_get(method, url):
    return DummyResponse(
        """{
                "result": "error",
                "error_info": "dummy informations"
        }"""
    )


def dummy_wrong_http_get(method, url):
    class DummyResponse:
        pass

    return DummyResponse()


@pytest.fixture
def client(scope="module", autouse=True):
    from app import app
    app.config['SECRET_KEY'] = DUMMY_JWT_SECRET_KEY
    return app.test_client()


# @pytest.fixture
# def expired_token():
#     payload = {
#         'exp': datetime.now() - timedelta(days=7)
#     }
#     token = jwt.encode(
#         payload,
#         DUMMY_JWT_SECRET_KEY,
#     )
#     return token


# @pytest.fixture
# def invalid_token():
#     payload = {
#         'exp': datetime.now() + timedelta(minutes=30)
#     }
#     token = jwt.encode(
#         payload,
#         DUMMY_JWT_SECRET_KEY + DUMMY_JWT_SECRET_KEY,
#     )
#     return token


# @pytest.fixture
# def valid_token():
#     payload = {
#         'exp': datetime.now() + timedelta(minutes=30)
#     }
#     token = jwt.encode(
#         payload,
#         DUMMY_JWT_SECRET_KEY,
#     )
#     return token


# @pytest.fixture
# def invalid_url(valid_token):
#     return (
#         f"/?token={valid_token}"
#         "&site_id=dummy_site"
#         "&token_auth=dummy_auth"
#     )


# @pytest.fixture
# def valid_url(valid_token):
#     return (
#         f"/?token={valid_token}"
#         "&id_site=dummy_site"
#         "&token_auth=dummy_auth"
#         "&base_url=dummy_url"
#         "&start_date=dummy_date"
#         "&db_name=dummy_name"
#     )


# @pytest.fixture
# def set_sent_file():
#     with open('dummy_name', 'wb'):
#         yield

#     os.remove('dummy_name')
