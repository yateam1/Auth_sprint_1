import json
import pytest

from app import config


@pytest.mark.social_tests
def test_success_get_authorization_code(test_app):
    client = test_app.test_client()
    params = {
        'client_id': config('MAILRU_CLIENT_ID'),
        'response_type': 'code',
        'scope': 'email',
        'redirect_uri': '/mailru/callback/',
    }

    resp = client.get(
        "https://oauth.mail.ru/login",
        params
    )
    print(resp)
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
