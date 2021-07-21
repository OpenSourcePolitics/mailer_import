import pytest
from mailer.main import get_user_list
from .utils import emails_file_setup, FILE_NAME

def test_get_user_list_file_not_found():
    with pytest.raises(FileNotFoundError):
        users = get_user_list(FILE_NAME + 'xxx')

def test_get_user_list_file_found():
    users = get_user_list(FILE_NAME)
    assert users