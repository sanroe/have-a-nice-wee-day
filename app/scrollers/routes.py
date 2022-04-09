from flask import Blueprint, render_template, request
from .models import Scroller, Customhaiku, Defaulthaiku, Mood, Longmessage

blueprint = Blueprint('scrollers', __name__)

@blueprint.route('/view/<slug>')
def view(slug):
    scroller = Scroller.query.filter_by(slug=slug).first_or_404()
    if scroller.customhaiku_id == None:
        haiku = Defaulthaiku.query.filter_by(id=scroller.defaulthaiku_id).first()
    else:
        haiku = Customhaiku.query.filter_by(id=scroller.customhaiku_id).first()
    msg = Longmessage.query.filter_by(id=scroller.longmessage_id).first()
    mood = Mood.query.filter_by(id=scroller.mood_id).first()
    return render_template('scrollers/view.html', scroller=scroller, haiku=haiku, msg=msg, mood=mood)

@blueprint.get('/create')
def get_create():
    return render_template('scrollers/create.html')

@blueprint.post('/create')
def post_create():
    # Create a scroller
    scroller = Scroller()
    scroller.save()

    return 'it was posted'

@blueprint.route('/404')
def error_404():
    return render_template('404.html')