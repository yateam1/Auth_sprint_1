import json
from uuid import uuid4

import pytest

from app.factories import UserFactory
from app.services import ProfileService

profile_service = ProfileService()


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
