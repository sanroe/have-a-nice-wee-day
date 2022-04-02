from flask import Flask
from . import scrollers, basic_pages
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    register_blueprints(app)

    return app

# Blueprints
def register_blueprints(app: Flask):
    app.register_blueprint(scrollers.routes.blueprint)
    app.register_blueprint(basic_pages.routes.blueprint)

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