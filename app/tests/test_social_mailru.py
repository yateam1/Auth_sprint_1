import pytest
import requests
import random
import string

from app import config


@pytest.mark.social_tests
def test_success_get_authorization_code(test_app):
    # client = test_app.test_client()
    params = {
        'client_id': config('MAILRU_CLIENT_ID'),
        'response_type': 'code',
        'redirect_uri': 'http://localhost:8000/',
        'state': ' ',
    }
    response = requests.get(
        "https://oauth.mail.ru/login",
        params=params,
    )
    print(response.content)

    assert response.status_code == 201
