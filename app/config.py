from dotenv import load_dotenv
from os import environ

load_dotenv()

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
FLASK_APP = environ.get('FLASK_APP')