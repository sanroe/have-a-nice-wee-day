from flask import Blueprint, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from app.scrollers.models import Scroller

blueprint = Blueprint('users', __name__)

@blueprint.get('/register')
def get_register():
    return render_template('users/register.html')

@blueprint.post('/register')
def post_register():
    try:
        if request.form.get('password') != request.form.get('password_confirmation'):
            return render_template('users/register.html', error='the password confirmation must match the password.')
        elif User.query.filter_by(email=request.form.get('email')).first():
            return render_template('users/register.html', error='the email address is already registered.')

        user = User(
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'))
        )
        user.save()

        login_user(user)
        return redirect(url_for('scrollers.myscrollers'))
    except Exception as error_message:
        error = error_message or 'an error occurred while creating your account. please make sure to enter valid data.'
        return render_template('users/register.html', error=error)

@blueprint.get('/login')
def get_login():
    return render_template('users/login.html')

@blueprint.post('/login')
def post_login():
    try:
        user = User.query.filter_by(email=request.form.get('email')).first()

        if not user:
            raise Exception('no user with that email address found.')
        elif check_password_hash(request.form.get('password'), user.password):
            raise Exception('the password is incorrect.')
        
        login_user(user)
        return redirect(url_for('scrollers.myscrollers'))
    
    except Exception as error_message:
        error = error_message or 'an error occurred while logging in. please verify your email and password.'
        return render_template('users/login.html', error=error)

@blueprint.get('/logout')
def logout():
    logout_user()

    return redirect(url_for('basic_pages.index'))

# Blueprint for user registration on first scroller creation
@blueprint.post('/success&<slug>&<logged_in>')
def post_success_register(slug, logged_in):
    try:
        if request.form.get('password') != request.form.get('password_confirmation'):
            return render_template('scrollers/success.html', slug=slug, logged_in=logged_in, error='the password confirmation must match the password.')
        elif User.query.filter_by(email=request.form.get('email')).first():
            return render_template('scrollers/success.html', slug=slug, logged_in=logged_in, error='the email address is already registered.')

        user = User(
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'))
        )
        user.save()
        
        login_user(user)

        scroller = Scroller.query.filter_by(slug=slug).first()
        scroller.user_id = user.id
        scroller.save()

        return redirect(url_for('scrollers.myscrollers'))
    except Exception as error_message:
        error = error_message or 'an error occurred while creating your account. please make sure to enter valid data.'
        return render_template('scrollers/success.html', slug=slug, logged_in=logged_in, error=error)