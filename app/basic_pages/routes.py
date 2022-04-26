from flask import Blueprint, render_template, redirect, url_for, send_file, session

blueprint = Blueprint('basic_pages', __name__)

@blueprint.route('/')
def index():
    # Attempt to fix bug on live site when logging in or registering
    session['slug'] = None
    return render_template('basic_pages/index.html')

@blueprint.route('/about')
def about():
    return render_template('basic_pages/about.html')

@blueprint.route('/legal')
def legal():
    return render_template('basic_pages/legal.html')

@blueprint.route('/404')
def error_404():
    return render_template('404.html')