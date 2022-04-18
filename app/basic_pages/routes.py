from flask import Blueprint, render_template, redirect, url_for, send_file

blueprint = Blueprint('basic_pages', __name__)

@blueprint.route('/')
def index():
    return render_template('basic_pages/index.html')

@blueprint.route('/about')
def about():
    return render_template('basic_pages/about.html')

@blueprint.route('/legal')
def legal():
    return render_template('basic_pages/legal.html')