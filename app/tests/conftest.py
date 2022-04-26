import pytest
from flask_migrate import upgrade
from os import environ
from app.app import create_app, talisman
from flask.testing import FlaskClient

@pytest.fixture(scope='module')
def flask_app():
    environ['DATABASE_URL'] = 'sqlite://'
    app = create_app()
    app.config['TESTING'] = True

    app = talisman(app)
    with app.app_context():
        upgrade()
        yield app

@pytest.fixture(scope='module')
def client(flask_app):
    app = flask_app
    ctx = flask_app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()