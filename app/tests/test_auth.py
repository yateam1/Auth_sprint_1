import json


def test_register(test_app):
    client = test_app.test_client()
    body = {
        'username': 'klimov4',
        'password': 'klimov',
        'email': 'klimov@klimov.ru'
    }

    resp = client.post("/auth/register", data=json.dumps(body), headers={"Content-Type": "application/json"})
    data = json.loads(resp.data.decode())

    assert body['username'] == body['username']
    assert resp.status_code == 201

