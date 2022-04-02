from flask import Blueprint, render_template

scroller_dummy_data = {
    'sarah': {'to-recipient-name': 'sarah', 'scroller-style': 'spring', 'scroller-colour': 'pastel', 'default-message': True, 'line-1': 'spring peeks through the clouds', 'line-2': 'I am reminded of you', 'line-3': 'and smile. you\'re the sun', 'long-message': 'wishing you well from across the way. hope to see you soon!', 'from-sender-name': 'you know who'},
    'laura': {'to-recipient-name': 'laura', 'scroller-style': 'spring', 'scroller-colour': 'pastel', 'default-message': True, 'line-1': 'spring peeks through the clouds', 'line-2': 'I am reminded of you', 'line-3': 'and smile. you\'re the sun', 'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'from-sender-name': 'you know who'}
}

blueprint = Blueprint('scrollers', __name__)

@blueprint.route('/view/<slug>')
def view(slug):
    if slug in scroller_dummy_data:
        return render_template('scrollers/view.html', scroller=scroller_dummy_data[slug])
    else:
        return render_template('scrollers/error.html')

@blueprint.route('/create')
def create():
    return render_template('scrollers/create.html')