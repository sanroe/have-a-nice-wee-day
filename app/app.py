from flask import Flask, redirect
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
from app.extensions.database import db, migrate
from app.extensions.authentication import login_manager
from . import scrollers, basic_pages, users
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    register_extensions(app)
    register_blueprints(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorised_page)

    return app

def talisman(app):
    # Disable https if app is run in testing mode
    force_https = False if app.config['TESTING'] else True

    Talisman(app, content_security_policy=GOOGLE_CSP_POLICY, force_https=force_https)
    return app

# Database
def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

# Blueprints
def register_blueprints(app: Flask):
    app.register_blueprint(scrollers.routes.blueprint)
    app.register_blueprint(basic_pages.routes.blueprint)
    app.register_blueprint(users.routes.blueprint)

# Page not found
def page_not_found(e):
    return redirect('/404')

def unauthorised_page(e):
    return redirect('/unauthorised')

# Logging

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Output to file settings
logfile = logging.FileHandler('file.log')
logfile.setLevel(logging.WARNING)
logfileformat = logging.Formatter('%(asctime)s - %(name)s - [%(filename)s > %(funcName)s() > %(lineno)s] - %(levelname)s - %(message)s')
logfile.setFormatter(logfileformat)

logger.addHandler(logfile)

# Output to console setting
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
streamformat = logging.Formatter('[%(levelname)s] %(message)s')
stream.setFormatter(streamformat)

logger.addHandler(stream)