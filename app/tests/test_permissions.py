import json
from uuid import uuid4

import pytest

from app.factories import RoleFactory


def test_create_role(test_app, test_db):
    client = test_app.test_client()
    role_data = {'name': 'admin'}
    resp = client.post(
        '/permissions/roles',
        data=json.dumps(role_data),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert f'Роль {role_data["name"]} добавлена.' == data['message']


def test_create_role_without_required_fields(test_app, test_db):
    client = test_app.test_client()
    resp = client.post(
        '/permissions/roles',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' == data['message']


def test_create_role_with_same_name(test_app, test_db):
    client = test_app.test_client()
    role = RoleFactory(name='admin')
    resp = client.post(
        '/permissions/roles',
        data=json.dumps({'name': 'admin'}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert f'Роль с именем {role.name} уже существует.' == data['message']


def test_get_correct_role(test_app, test_db):
    role = RoleFactory()
    client = test_app.test_client()
    resp = client.get(f'/permissions/roles/{role.id}', content_type='application/json')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert {
        'id': str(role.id),
        'name': role.name,
        'created': role.created.isoformat(),
        'updated': role.updated,
    } == data

def test_get_incorrect_role(test_app, test_db):
    role_id = uuid4()
    client = test_app.test_client()
    resp = client.get(f'permissions/roles/{role_id}', content_type='application/json')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert f'Роли {role_id} не существует.' == data['message']


@pytest.mark.parametrize('count', [1, 10, 0])
def test_get_list_roles(test_app, test_db, count):
    RoleFactory.create_batch(count)
    client = test_app.test_client()
    resp = client.get(f'permissions/roles', content_type='application/json')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert count == len(data)
