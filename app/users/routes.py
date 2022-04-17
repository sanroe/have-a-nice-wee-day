from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash, check_password_hash

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

        return 'User created'
    except Exception as error_message:
        error = error_message or 'an error occurred while creating your account. please make sure to enter valid data.'
        return render_template('users/register.html', error=error)

@blueprint.get('/login')
def get_login():
    return render_template('users/login.html')

@blueprint.post('/login')
def post_login():
    return 'User logged in'

@blueprint.get('/logout')
def logout():
    return 'User logged out'