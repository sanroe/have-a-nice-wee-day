from flask import Flask, redirect, url_for, render_template, send_file

app = Flask(__name__)
app.config.from_object('app.config')

scroller_dummy_data = {
    'sarah': {'to-recipient-name': 'sarah', 'scroller-style': 'spring', 'scroller-colour': 'pastel', 'default-message': True, 'line-1': 'spring peeks through the clouds', 'line-2': 'I am reminded of you', 'line-3': 'and smile. you\'re the sun', 'long-message': 'wishing you well from across the way. hope to see you soon!', 'from-sender-name': 'you know who'},
    'laura': {'to-recipient-name': 'laura', 'scroller-style': 'spring', 'scroller-colour': 'pastel', 'default-message': True, 'line-1': 'spring peeks through the clouds', 'line-2': 'I am reminded of you', 'line-3': 'and smile. you\'re the sun', 'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'from-sender-name': 'you know who'}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/view/<slug>')
def view(slug):
    if slug in scroller_dummy_data:
        return render_template('view.html', scroller=scroller_dummy_data[slug])
    else:
        return 'Sorry, could not find that scroller.'