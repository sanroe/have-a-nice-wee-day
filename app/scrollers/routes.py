from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from .models import Scroller, Customhaiku, Defaulthaiku, Mood, Longmessage
from flask_login import login_required, current_user
from .utils import create_unique_slug

blueprint = Blueprint('scrollers', __name__)

# Route for the sender to view and edit
@blueprint.route('/view/<slug>')
def view_edit(slug):
    # Only allow view to edit of scroller if logged in user matches or if slug matches authored from session, otherwise throw unauthorised error
    # Avoids eg, a different logged in user being able to edit scroller by adding '/view/ to known URL
    scroller = Scroller.query.filter_by(slug=slug).first_or_404()
    try:
        if session['authored'] == slug or int(current_user.get_id()) == scroller.user_id:
            if scroller.customhaiku_id == None:
                haiku = Defaulthaiku.query.filter_by(id=scroller.defaulthaiku_id).first()
            else:
                haiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
            line_one = haiku.line_one.split()
            line_two = haiku.line_two.split()
            line_three = haiku.line_three.split()
            msg = ''
            if scroller.longmessage_id:
                msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
                msg = msg.msg.splitlines(True)
            mood = Mood.query.filter_by(id=scroller.mood_id).first()
            mood_name = mood.name
            edit_allowed = True
            return render_template('scrollers/view.html', scroller=scroller, line_one=line_one, line_two=line_two, line_three=line_three, msg=msg, mood=mood_name, edit_allowed=edit_allowed)
    except:
        return render_template('unauthorised.html')

# Route for the recipient to view only
@blueprint.route('/<slug>')
def view(slug):
    scroller = Scroller.query.filter_by(slug=slug).first_or_404()
    if scroller.customhaiku_id == None:
        haiku = Defaulthaiku.query.filter_by(id=scroller.defaulthaiku_id).first()
    else:
        haiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
    line_one = haiku.line_one.split()
    line_two = haiku.line_two.split()
    line_three = haiku.line_three.split()
    msg = ''
    if scroller.longmessage_id:
        msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
        msg = msg.msg.splitlines(True)
    mood = Mood.query.filter_by(id=scroller.mood_id).first()
    mood_name = mood.name
    edit_allowed = False
    return render_template('scrollers/view.html', scroller=scroller, line_one=line_one, line_two=line_two, line_three=line_three, msg=msg, mood=mood_name, edit_allowed=edit_allowed)

@blueprint.get('/create')
def get_create():
    return render_template('scrollers/create.html')

@blueprint.post('/create')
def post_create():    
    try:
        # Validate required fields
        if not all ([
            request.form.get('to-recipient-name'),
            request.form.get('mood'),
            request.form.get('default-message'),
            request.form.get('from-sender-name')
        ]):
            raise Exception('please fill in all required fields!')
        
        if request.form.get('default-message') == 'False':
            if not all ([
                request.form.get('line-one'),
                request.form.get('line-two'),
                request.form.get('line-three')
            ]):
                raise Exception('please complete your haiku!')

        # Clean to and from names to lowercase
        to_name = request.form.get('to-recipient-name').lower()
        from_name = request.form.get('from-sender-name').lower()

        # Create a unique slug
        slug = create_unique_slug(request.form.get('to-recipient-name'))

        # Create a new scroller
        scroller = Scroller(
            slug=slug,
            to_recipient_name=to_name,
            from_sender_name=from_name,
            mood_id=request.form.get('mood')
        )
        scroller.save()

        # Either create custom haiku entry or update scroller with default
        if request.form.get('default-message') == "False":
            customhaiku = Customhaiku(
                line_one=request.form.get('line-one'),
                line_two=request.form.get('line-two'),
                line_three=request.form.get('line-three')
            )
            customhaiku.save()
            scroller.customhaiku_id = customhaiku.id
            scroller.save()
        elif request.form.get('default-message') == "True":
            scroller.defaulthaiku_id = request.form.get('mood')
            scroller.save()

        longmessage = Longmessage(
            msg=request.form.get('long-message')
            )
        longmessage.save()
        scroller.longmessage_id = longmessage.id
        scroller.save()

        logged_in = False

        # Save user if logged in
        if current_user.is_authenticated:
            user = int(current_user.get_id())
            scroller.user_id = user
            scroller.save()
            logged_in = True

        session['slug'] = slug
        session['logged_in'] = logged_in
        # Store slug of current scroller in session to check if authored when attempting to edit
        session['authored'] = slug

        return redirect(url_for('scrollers.success'))
    except Exception as error_message:
        error = error_message or 'An error occurred while trying to create your scroller. Please try again.'
        
        current_app.logger.info(f'Error creating a scroller: {error}')

        return render_template('scrollers/create.html', error=error)

@blueprint.route('/success')
def success():
    slug = session['slug']
    logged_in = session['logged_in']
    site_url = request.url_root
    return render_template('scrollers/success.html', slug=slug, logged_in=logged_in, has_account=False, site_url=site_url)
    
# Route save scroller and log in if already have an account but not logged in
@blueprint.route('/success/login')
def success_not_logged_in_with_account():
    slug = session['slug']
    logged_in = session['logged_in']
    site_url = request.url_root
    return render_template('scrollers/success.html', slug=slug, logged_in=logged_in, has_account=True, site_url=site_url)

@blueprint.route('/myscrollers')
@login_required
def myscrollers():
    page_number = request.args.get('page', 1, type=int)
    user = int(current_user.get_id())
    my_scrollers_pagination = Scroller.query.filter_by(user_id=user).paginate(page_number, current_app.config['SCROLLERS_PER_PAGE'])
    return render_template('scrollers/index.html', my_scrollers_pagination=my_scrollers_pagination)

@blueprint.route('/delete/<slug>')
@login_required
def delete_scroller(slug):
    scroller = Scroller.query.filter_by(slug=slug).first()
    # Only delete scroller is logged in user matches otherwise throw unauthorised error
    # Avoids eg, a different logged in user being able to delete scroller by editing known URL
    if int(current_user.get_id()) == scroller.user_id:
        if scroller.customhaiku_id != None:
            customhaiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
            customhaiku.delete()
        if scroller.longmessage_id != None:
            longmessage = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
            longmessage.delete()
        scroller.delete()
        return redirect(url_for('scrollers.myscrollers'))
    else:
        return render_template('unauthorised.html')

@blueprint.get('/edit/<slug>')
def get_edit_scroller(slug):
    scroller = Scroller.query.filter_by(slug=slug).first()
    # Only allow view to edit of scroller if logged in user matches or if slug matches authored from session, otherwise throw unauthorised error
    # Avoids eg, a different logged in user being able to edit scroller by adding '/view/ to known URL
    try:
        if session['authored'] == slug or int(current_user.get_id()) == scroller.user_id:
            if scroller.customhaiku_id != None:
                haiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
                default_haiku = False
            else:
                haiku = Defaulthaiku.query.filter_by(id=scroller.defaulthaiku_id).first()
                default_haiku = True
            msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
            mood = Mood.query.filter_by(id=scroller.mood_id).first()
            return render_template('scrollers/edit.html', scroller=scroller, haiku=haiku, msg=msg, mood=mood, default_haiku=default_haiku)
    except:
        return render_template('unauthorised.html')

@blueprint.post('/edit/<slug>')
def post_edit_scroller(slug):    
    try:
        # Validate required fields
        if not all ([
            request.form.get('to-recipient-name'),
            request.form.get('mood'),
            request.form.get('default-message'),
            request.form.get('from-sender-name')
        ]):
            raise Exception('please fill in all required fields!')
        
        if request.form.get('default-message') == 'False':
            if not all ([
                request.form.get('line-one'),
                request.form.get('line-two'),
                request.form.get('line-three')
            ]):
                raise Exception('please complete your haiku!')

        # Clean to and from names to lowercase
        to_name = request.form.get('to-recipient-name').lower()
        from_name = request.form.get('from-sender-name').lower()

        # Grab scroller record and update
        scroller = Scroller.query.filter_by(slug=slug).first()
        scroller.to_recipient_name = to_name
        scroller.from_sender_name = from_name
        scroller.mood_id = request.form.get('mood')
        scroller.save()

        # Either update custom haiku entry (if exists or save new) or update scroller as default (deleting previous custom haiku entry)
        if request.form.get('default-message') == "False" and scroller.customhaiku_id:
            customhaiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
            customhaiku.line_one = request.form.get('line-one')
            customhaiku.line_two = request.form.get('line-two')
            customhaiku.line_three = request.form.get('line-three')
            customhaiku.save()
        elif request.form.get('default-message') == "False" and not scroller.customhaiku_id:
            customhaiku = Customhaiku(
                line_one=request.form.get('line-one'),
                line_two=request.form.get('line-two'),
                line_three=request.form.get('line-three')
            )
            customhaiku.save()
            scroller.customhaiku_id = customhaiku.id
            scroller.save()
        elif request.form.get('default-message') == "True" and scroller.customhaiku_id:
            customhaiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
            customhaiku.delete()
            scroller.customhaiku_id = None
            scroller.defaulthaiku_id = request.form.get('mood')
            scroller.save()

        # Update existing long message or save new if not exists
        if scroller.longmessage_id and request.form.get('long-message'):
            longmessage = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
            longmessage.msg = request.form.get('long-message')
            longmessage.save()
        elif scroller.longmessage_id and not request.form.get('long-message'):
            longmessage = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
            longmessage.delete()
            scroller.longmessage_id = None
            scroller.save()
        elif not scroller.longmessage_id:
            longmessage = Longmessage(
                msg=request.form.get('long-message')
                )
            print(longmessage)
            longmessage.save()
            scroller.longmessage_id = longmessage.id
            scroller.save()

        has_account = ''

        # Check whether logged in
        if current_user.is_authenticated:
            logged_in = True
        else:
            logged_in = False
            has_account = False

        site_url = request.url_root

        return render_template('scrollers/success.html', slug=slug, logged_in=logged_in, has_account=has_account, site_url=site_url)
    except Exception as error_message:
        error = error_message or 'an error occurred while trying to update your scroller. maybe start afresh.'
        
        current_app.logger.info(f'error updating a scroller: {error}')

        return render_template('scrollers/create.html', error=error)