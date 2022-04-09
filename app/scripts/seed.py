from app.app import create_app
from app.scrollers.models import Defaulthaiku, Mood, Scroller, Longmessage
from app.extensions.database import db

app = create_app()
app.app_context().push()

defaulthaiku_data = {
    'spring': {'line_one': 'spring peeks through the clouds', 'line_two': 'I am reminded of you', 'line_three': 'and smile. you\'re the sun'},
    'autumn': {'line_one': 'seasons change, leaves fall', 'line_two': 'a soft breeze, I think of you', 'line_three': 'and the light you bring'}
}

for key, value in defaulthaiku_data.items():
    new_defaulthaiku = Defaulthaiku(name=key, line_one=value['line_one'], line_two=value['line_two'], line_three=value['line_three'])
    db.session.add(new_defaulthaiku)

mood_data = ['spring', 'autumn']

for each in mood_data:
    new_mood = Mood(name=each)
    db.session.add(new_mood)

scroller_test_data = {
    'test-slug-sarah': { 'to_recipient_name': 'sarah', 'from_sender_name': ':)', 'defaulthaiku_id': '1', 'longmessage_id': '1', 'mood_id': '1'},
    'test-slug-laura': { 'to_recipient_name': 'laura', 'from_sender_name': ':)', 'defaulthaiku_id': '2', 'longmessage_id': '2', 'mood_id': '2'},
}

for key, value in scroller_test_data.items():
    new_scroller = Scroller(slug=key, to_recipient_name=value['to_recipient_name'], from_sender_name=value['from_sender_name'], defaulthaiku_id=value['defaulthaiku_id'], longmessage_id=value['longmessage_id'], mood_id=value['mood_id'])
    db.session.add(new_scroller)

longmessage_data = {
    'test-slug-sarah': {'msg': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'},
    'test-slug-laura': {'msg': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'}
}

for key, value in longmessage_data.items():
    new_longmessage = Longmessage(msg=value['msg'])
    db.session.add(new_longmessage)

db.session.commit()