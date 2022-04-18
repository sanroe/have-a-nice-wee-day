from flask import Blueprint, render_template, request, current_app, redirect, url_for
from .models import Scroller, Customhaiku, Defaulthaiku, Mood, Longmessage
from flask_login import login_required, current_user
import secrets
import string

blueprint = Blueprint('scrollers', __name__)

# Route for the sender to view and edit
@blueprint.route('/view/<slug>')
def view_edit(slug):
    scroller = Scroller.query.filter_by(slug=slug).first_or_404()
    if scroller.customhaiku_id == None:
        haiku = Defaulthaiku.query.filter_by(id=scroller.defaulthaiku_id).first()
    else:
        haiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
    line_one = haiku.line_one.split()
    line_two = haiku.line_two.split()
    line_three = haiku.line_three.split()
    msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
    msg = msg.msg.splitlines(True)
    mood = Mood.query.filter_by(id=scroller.mood_id).first()
    edit_allowed = True
    return render_template('scrollers/view.html', scroller=scroller, line_one=line_one, line_two=line_two, line_three=line_three, msg=msg, mood=mood, edit_allowed=edit_allowed)

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
    msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
    msg = msg.msg.splitlines(True)
    mood = Mood.query.filter_by(id=scroller.mood_id).first()
    edit_allowed = False
    return render_template('scrollers/view.html', scroller=scroller, line_one=line_one, line_two=line_two, line_three=line_three, msg=msg, mood=mood, edit_allowed=edit_allowed)

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
        to_name = request.form.get('to-recipient-name')
        from_name = request.form.get('from-sender-name')
        to_name_lower = to_name.lower()
        from_name_lower = from_name.lower()

        # Create a unique slug
        slug_prefix = to_name_lower.replace(" ", "-")
        slug_suffix = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(20))
        slug = slug_prefix + '-' + slug_suffix

        # Create a new scroller
        scroller = Scroller(
            slug=slug,
            to_recipient_name=to_name_lower,
            from_sender_name=from_name_lower,
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

        # Save user if logged in
        if current_user.is_authenticated:
            user = int(current_user.get_id())
            scroller.user_id = user
            scroller.save()

        return render_template('scrollers/success.html', slug=slug)
    except Exception as error_message:
        error = error_message or 'An error occurred while trying to create your scroller. Please try again.'
        
        current_app.logger.info(f'Error creating a scroller: {error}')

        return render_template('scrollers/create.html', error=error)

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
    if scroller.customhaiku_id != None:
        customhaiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
        customhaiku.delete()
    if scroller.longmessage_id != None:
        longmessage = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
        longmessage.delete()
    scroller.delete()
    return redirect(url_for('scrollers.myscrollers'))

@blueprint.get('/edit/<slug>')
def get_edit_scroller(slug):
    scroller = Scroller.query.filter_by(slug=slug).first()
    if scroller.customhaiku_id != None:
        haiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
        default_haiku = False
    else:
        haiku = Defaulthaiku.query.filter_by(id=scroller.defaulthaiku_id).first()
        default_haiku = True
    msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
    mood = Mood.query.filter_by(id=scroller.mood_id).first()
    return render_template('scrollers/edit.html', scroller=scroller, haiku=haiku, msg=msg, mood=mood, default_haiku=default_haiku)

@blueprint.route('/404')
def error_404():
    return render_template('404.html')

@blueprint.route('/unauthorised')
def error_401():
    return render_template('unauthorised.html')