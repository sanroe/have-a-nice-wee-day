from flask import Flask, redirect
from app.extensions.database import db, migrate
from . import scrollers, basic_pages, users
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    register_extensions(app)
    register_blueprints(app)

    app.register_error_handler(404, page_not_found)

    return app

# Database
def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)

# Blueprints
def register_blueprints(app: Flask):
    app.register_blueprint(scrollers.routes.blueprint)
    app.register_blueprint(basic_pages.routes.blueprint)
    app.register_blueprint(users.routes.blueprint)

# Page not found
def page_not_found(e):
    return redirect('/404')

# Logging

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Output to file settings
logfile = logging.FileHandler('file.log')
logfile.setLevel(logging.INFO)
logfileformat = logging.Formatter('%(asctime)s - %(name)s - [%(filename)s > %(funcName)s() > %(lineno)s] - %(levelname)s - %(message)s')
logfile.setFormatter(logfileformat)

logger.addHandler(logfile)

# Output to console setting
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
streamformat = logging.Formatter('[%(levelname)s] %(message)s')
stream.setFormatter(streamformat)

logger.addHandler(stream)