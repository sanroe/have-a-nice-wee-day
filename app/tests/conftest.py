import pytest
from os import environ
from app.app import create_app

@pytest.fixture
def client():
    environ['DATABASE_URL'] = 'sqlite://'
    app = create_app()

    with app.app_context():
        yield app.test_client()