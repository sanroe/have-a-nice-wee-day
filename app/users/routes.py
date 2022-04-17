from flask import Blueprint, render_template

blueprint = Blueprint('users', __name__)

@blueprint.get('/register')
def get_register():
    return render_template('users/register.html')

@blueprint.post('/register')
def post_register():
    if request.form.get('password') != request.form.get('password_confirmation'):
        return render_template('users/register.html', error='the password confirmation must match the password.')
    elif User.query.filter_by(email=request.form.get('email')).first():
        return render_template('users/register.html', error='the email address is already registered.')

    return 'User created'

@blueprint.get('/login')
def get_login():
    return render_template('users/login.html')

@blueprint.post('/login')
def post_login():
    return 'User logged in'

@blueprint.get('/logout')
def logout():
    return 'User logged out'