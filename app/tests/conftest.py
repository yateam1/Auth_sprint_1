import pytest

from app import create_app, db
from app.factories import HeaderFactory, UserFactory
from app.models import User


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("app.settings.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture
def test_db():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def auth_headers():
    return HeaderFactory().headers


@pytest.fixture
def user_headers(auth_headers):
    user = UserFactory(password='password')
    auth_headers['Authorization'] = user.encode_token()
    return auth_headers


def get_user_id_from_token(token: str) -> dict:
    return User.decode_token(token)['user_id']
