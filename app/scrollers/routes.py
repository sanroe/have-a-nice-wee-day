from flask import Blueprint, render_template
from .models import Scroller, Customhaiku, Defaulthaiku, Mood, Longmessage

scroller_dummy_data = {
    'sarah': {'to-recipient-name': 'sarah', 'scroller-style': 'spring', 'scroller-colour': 'pastel', 'default-message': True, 'line-1': 'spring peeks through the clouds', 'line-2': 'I am reminded of you', 'line-3': 'and smile. you\'re the sun', 'long-message': 'wishing you well from across the way. hope to see you soon!', 'from-sender-name': 'you know who'},
    'laura': {'to-recipient-name': 'laura', 'scroller-style': 'spring', 'scroller-colour': 'pastel', 'default-message': True, 'line-1': 'spring peeks through the clouds', 'line-2': 'I am reminded of you', 'line-3': 'and smile. you\'re the sun', 'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'from-sender-name': 'you know who'}
}

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

@blueprint.route('/create')
def create():
    return render_template('scrollers/create.html')

@blueprint.route('/404')
def error_404():
    return render_template('404.html')