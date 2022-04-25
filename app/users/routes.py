from flask import Blueprint, render_template, request, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
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

        # If user registers in through navbar during active scroller creation session, automatically save to account
        if session['slug']:
            slug = session['slug']
            scroller = Scroller.query.filter_by(slug=slug).first()
            scroller.user_id = user.id
            scroller.save()
            # Reset session attribute to falsey to fix bug on login and outs later
            session['slug'] = None

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

        # If user logins in through navbar during active scroller creation session, automatically save to account
        if session['slug']:
            slug = session['slug']
            scroller = Scroller.query.filter_by(slug=slug).first()
            scroller.user_id = user.id
            scroller.save()
            # Reset session attribute to falsey to fix bug on login and outs later
            session['slug'] = None

        return redirect(url_for('scrollers.myscrollers'))
    
    except Exception as error_message:
        error = error_message or 'an error occurred while logging in. please verify your email and password.'
        return render_template('users/login.html', error=error)

@blueprint.get('/logout')
def logout():
    logout_user()
    # Reset session attribute to falsey to fix bug on login and outs later
    session['slug'] = None

    return redirect(url_for('basic_pages.index'))

# Blueprint for user registration on first scroller creation
@blueprint.post('/success')
def post_success_register():
    try:
        slug = session['slug']
        if request.form.get('password') != request.form.get('password_confirmation'):
            return render_template('scrollers/success.html', slug=slug, logged_in=session['logged_in'], has_account=False, error='the password confirmation must match the password.')
        elif User.query.filter_by(email=request.form.get('email')).first():
            return render_template('scrollers/success.html', slug=session['slug'], logged_in=session['logged_in'], has_account=False, error='the email address is already registered.')

        user = User(
            email=request.form.get('email'),
            password=generate_password_hash(request.form.get('password'))
        )
        user.save()
        login_user(user)

        scroller = Scroller.query.filter_by(slug=slug).first()
        scroller.user_id = user.id
        scroller.save()
        # Reset session attribute to falsey to fix bug on login and outs later
        session['slug'] = None

        return redirect(url_for('scrollers.myscrollers'))
    except Exception as error_message:
        error = error_message or 'an error occurred while creating your account. please make sure to enter valid data.'
        return render_template('scrollers/success.html', slug=session['slug'], logged_in=session['logged_in'], has_account=False, error=error)

# Blueprint for user login on scroller creation
@blueprint.post('/success/login')
def post_success_login():
    try:
        slug = session['slug']
        user = User.query.filter_by(email=request.form.get('email')).first()

        if not user:
            raise Exception('no user with that email address found.')
        elif check_password_hash(request.form.get('password'), user.password):
            raise Exception('the password is incorrect.')

        login_user(user)

        scroller = Scroller.query.filter_by(slug=slug).first()
        scroller.user_id = user.id
        scroller.save()
        # Reset session attribute to falsey to fix bug on login and outs later
        session['slug'] = None

        return redirect(url_for('scrollers.myscrollers'))
    except Exception as error_message:
        error = error_message or 'an error occurred while trying to log you in. please make sure to enter valid data.'
        return render_template('scrollers/success.html', slug=session['slug'], logged_in=session['logged_in'], has_account=True, error=error)

# Blueprint for managing account
@blueprint.get('/manage')
@login_required
def get_manage_account():
    user_id = int(current_user.get_id())
    user = User.query.filter_by(id=user_id).first()
    return render_template('users/manage.html', user=user)

@blueprint.post('/manage')
@login_required
def post_manage_account():
    user_id = int(current_user.get_id())
    user = User.query.filter_by(id=user_id).first()
    try:
        if request.form.get('email'):
            if User.query.filter_by(email=request.form.get('email')).first():
                return render_template('users/manage.html', error='the email address is registered to someone else.')
            else:
                user.email = request.form.get('email')
                user.save()
        if request.form.get('password'):
            if request.form.get('password') != request.form.get('password_confirmation'):
                return render_template('users/manage.html', error='the password confirmation must match the password.')
            else:
                user.password=generate_password_hash(request.form.get('password'))
                user.save()
        login_user(user)
        confirmation_message = "done!"
        return render_template('users/manage.html', user=user, confirmation_message=confirmation_message)
    except Exception as error_message:
        error = error_message or 'an error occurred while trying to update your details. please make sure to enter valid data.'
        return render_template('users/manage.html', user=user, error=error)

# Blueprint for unauthorised actions, 401 error
@blueprint.route('/unauthorised')
def error_401():
    return render_template('unauthorised.html')