import json

from .conftest import body, headers, USER_AGENT, FINGERPRINT


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
    assert len(data['access_token']) == 231
    assert len(data['refresh_token']) == 36
    assert resp.status_code == 200
