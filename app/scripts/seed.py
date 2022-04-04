from app.app import create_app
from app.scrollers.models import Defaulthaiku, Mood
from app.extensions.database import db

app = create_app()
app.app_context().push()

defaulthaiku_data = {
    'spring': {'line_one': 'spring peeks through the clouds', 'line_two': 'I am reminded of you', 'line_three': 'and smile. you\'re the sun'},
    'autumn': {'line_one': 'seasons change, leaves fall', 'line_two': 'a soft breeze, I think of you', 'line_three': 'and the light you bring'}
}

mood_data = ['spring', 'autumn']

for key, value in defaulthaiku_data.items():
    new_defaulthaiku = Defaulthaiku(name=key, line_one=value['line_one'], line_two=value['line_two'], line_three=value['line_three'])
    db.session.add(new_defaulthaiku)

for each in mood_data:
    new_mood = Mood(name=each)
    db.session.add(new_mood)

db.session.commit()