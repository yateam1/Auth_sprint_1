import pytest

from app import create_app

USER_AGENT = 'test app for auth'
FINGERPRINT = 'Noname device'

body = {
    'username': 'klimov4',
    'password': 'klimov',
    'email': 'klimov@klimov.ru',
}

headers = {
    "Content-Type": "application/json",
}


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("app.settings.TestingConfig")
    with app.app_context():
        yield app
