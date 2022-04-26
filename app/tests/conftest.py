import pytest
from flask_migrate import upgrade
from os import environ
from app.app import create_app, talisman

@pytest.fixture
def client():
    environ['DATABASE_URL'] = 'sqlite://'
    app = create_app()
    app.config['TESTING'] = True

    app = talisman(app)

    with app.app_context():
        upgrade()
        yield app.test_client()