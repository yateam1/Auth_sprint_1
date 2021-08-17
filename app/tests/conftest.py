import pytest

from app import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("app.settings.TestingConfig")
    with app.app_context():
        yield app
