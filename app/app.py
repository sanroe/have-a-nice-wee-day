from flask import Flask
from . import scrollers, basic_pages

app = Flask(__name__)
app.config.from_object('app.config')

# Blueprints
app.register_blueprint(scrollers.routes.blueprint)
app.register_blueprint(basic_pages.routes.blueprint)