import pytest

from app import create_app, db
from app.factories import HeaderFactory


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
