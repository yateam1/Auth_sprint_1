import json

from .conftest import body, headers, USER_AGENT, FINGERPRINT
from ..services import SessionService, UserService


def test_register(test_app):
    client = test_app.test_client()

    resp = client.post("/auth/register", data=json.dumps(body), headers=headers)
    data = json.loads(resp.data.decode())

    if resp.status_code == 201:
        assert body['username'] == data['username']
    assert resp.status_code in [201, 400]   # Пользователь либо создан, либо уже существует


def test_login(test_app):
    client = test_app.test_client()
    headers['User-Agent'] = USER_AGENT
    headers['fingerprint'] = FINGERPRINT

    resp = client.post("/auth/login", data=json.dumps(body), headers=headers)
    data = json.loads(resp.data.decode())
    assert resp.status_code in [200, 401]

    if resp.status_code == 200:
        assert len(data['access_token']) == 231
        assert len(data['refresh_token']) == 231
    else:
        assert data['message'].find('Пользователь уже залогинен') != -1


def test_refresh_token(test_app):
    client = test_app.test_client()
    headers['User-Agent'] = USER_AGENT
    headers['fingerprint'] = FINGERPRINT

    session_service = SessionService()
    user_service = UserService()

    user = user_service.get_user_by_username(body['username'])
    session = session_service.get_by_user(user=user, fingerprint=FINGERPRINT, user_agent=USER_AGENT)

    resp = client.post("/auth/refresh-tokens",
                       data=json.dumps({'refresh_token' : session.refresh_token}),
                       headers=headers)
    data = json.loads(resp.data.decode())
    assert resp.status_code in [201, 401]

    if resp.status_code == 201:
        assert len(data['access_token']) == 231
        assert len(data['refresh_token']) == 231
    else:
        assert data['message'].find('Пользователь уже залогинен') != -1