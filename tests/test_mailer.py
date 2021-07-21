from mailer.mailjet import Mailjet
from mailer.sendlinblue import Sendinblue
from .utils import (
    emails_for_test,
    DummyMailerWorking,
    DUMMY_MAILJET_ANSWER
)
import pytest

@pytest.mark.parametrize("mailer",[Mailjet, Sendinblue])
def test_mailer_api_keys_wrong(mailer, monkeypatch):
    monkeypatch.setattr(mailer, 'setup', DummyMailerWrongEnv)
    mailer.setup()

    response = mailer.message.get()
    assert not response.ok
    assert response.status_code == 401


@pytest.mark.parametrize("mailer", [Mailjet, Sendinblue])
def test_mailer_address_not_found(mailer, monkeypatch):
    monkeypatch.settattr(mailer, 'setup', DummyMailerWorking)
    mailer.setup()

    response = mailer.message.get()
    assert response.ok
    assert response.status_code == 200


@pytest.mark.parametrize(
    "mailer,expected_answer",
    [(Mailjet, DUMMY_MAILJET_ANSWER), (Sendinblue, DUMMY_SIB_ANSWER)]
)
def test_mailer_address_found(mailer, expected_answer, monkeypatch):
    monkeypatch.settattr(mailer, 'setup', DummyMailerWorking)
    mailer.setup()

    response = mailer.message.get()
    assert response.content == expected_answer


@pytest.mark.parametrize(
    "mailer, parsed_message",
    [(Mailjet,DUMMY_PARSED_MESSAGE_MAILJET),(Sendinblue, DUMMY_PARSED_MESSAGE_SENDINBLUE)]
)
def test_mailjet_address_correct_parse_message(mailer, parsed_message, monkeypatch):
    monkeypatch.settattr(mailer, 'setup', DummyMailerWorking)
    mailer.setup()

    parsed_message = Mailjet().parse_message(address_data)
    assert parsed_message.keys().sort() == [
        'sender',
        'email',
        'opened',
        'clicked',
        'sent_at'
    ]
