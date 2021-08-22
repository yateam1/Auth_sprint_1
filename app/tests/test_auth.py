import json

import pytest

from app.factories import UserFactory
from app.services import ProfileService, SessionService

profile_service = ProfileService()
session_service = SessionService()


def test_register_user(test_app, test_db):
    client = test_app.test_client()
    user_data = {
        'username': 'we1tkind',
        'email': 'sa@prg.re',
        'password': 'qwerty',
    }
    resp = client.post(
        '/auth/register',
        data=json.dumps(user_data),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    profile = profile_service.get_by_email(user_data['email'])
    assert profile is not None
    assert resp.status_code == 201
    assert user_data['username'] == data['username']


def test_register_user_with_same_username(test_app, test_db):
    client = test_app.test_client()
    user = UserFactory(password='123', username='user')
    user_data = {
        'username': user.username,
        'email': 'sa@prg.re',
        'password': 'qwerty',
    }
    resp = client.post(
        '/auth/register',
        data=json.dumps(user_data),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert f'Пользователь {user_data["username"]} уже зарегистрирован.' == data['message']


@pytest.mark.parametrize(
    'payload',
    [{'email': 'sa@prg.re', 'password': 'qwerty'},
     {'email': 'sa@prg.re', 'username': 'qwerty'},
     {},
     {'username': 'qwerty'},
     ],
)
def test_register_user_without_required_data(test_app, test_db, payload):
    client = test_app.test_client()
    resp = client.post(
        '/auth/register',
        data=json.dumps(payload),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' == data['message']


@pytest.mark.parametrize(
    'headers',
    [{}, {'User-Agent': 'user_agent'}],
)
def test_auth_user_without_required_headers(test_app, test_db, headers):
    client = test_app.test_client()
    user_data = {
        'username': 'we1tkind',
        'password': 'qwerty',
    }
    resp = client.post(
        '/auth/login',
        content_type='application/json',
        data=json.dumps(user_data),
        headers=headers
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Не переданы обязательные заголовки.' == data['message']


@pytest.mark.parametrize(
    'payload',
    [{'username': 'we1tkind'}, {'password': 'qwerty'}, {}],
)
def test_auth_user_without_required_fields(test_app, test_db, auth_headers, payload):
    client = test_app.test_client()
    resp = client.post(
        '/auth/login',
        content_type='application/json',
        data=json.dumps(payload),
        headers=auth_headers
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' == data['message']


def test_auth_user(test_app, test_db, auth_headers):
    client = test_app.test_client()
    user = UserFactory(password='password')
    user_auth_data = {
        'username': user.username,
        'password': 'password',
    }
    resp = client.post(
        '/auth/login',
        content_type='application/json',
        data=json.dumps(user_auth_data),
        headers=auth_headers
    )
    data = json.loads(resp.data.decode())
    assert session_service.get_by_user(user, auth_headers['Fingerprint'], auth_headers['User-Agent']) is not None
    assert resp.status_code == 200
    assert 'access_token' in data.keys()
    assert 'refresh_token' in data.keys()


def test_auth_incorrect_user(test_app, test_db, auth_headers):
    client = test_app.test_client()
    user_auth_data = {
        'username': 'username',
        'password': 'password',
    }
    resp = client.post(
        '/auth/login',
        content_type='application/json',
        data=json.dumps(user_auth_data),
        headers=auth_headers
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'Пользователя не существует.' in data['message']


def test_auth_user_with_incorrect_password(test_app, test_db, auth_headers):
    client = test_app.test_client()
    user = UserFactory(password='password')
    user_auth_data = {
        'username': user.username,
        'password': 'pass___word',
    }
    resp = client.post(
        '/auth/login',
        content_type='application/json',
        data=json.dumps(user_auth_data),
        headers=auth_headers
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'Неверный пароль.' in data['message']