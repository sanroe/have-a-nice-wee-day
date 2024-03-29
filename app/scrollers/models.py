from app.extensions.database import db, CRUDMixin

class Scroller(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    to_recipient_name = db.Column(db.String(80))
    from_sender_name = db.Column(db.String(80))
    customhaiku_id = db.Column(db.Integer, db.ForeignKey('customhaiku.id'))
    defaulthaiku_id = db.Column(db.Integer, db.ForeignKey('defaulthaiku.id'))
    longmessage_id = db.Column(db.Integer, db.ForeignKey('longmessage.id'))
    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Customhaiku(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    line_one = db.Column(db.String(255))
    line_two = db.Column(db.String(255))
    line_three = db.Column(db.String(255))
    scroller = db.relationship('Scroller', backref='customhaiku', uselist=False, lazy=True)

class Defaulthaiku(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    line_one = db.Column(db.String(255))
    line_two = db.Column(db.String(255))
    line_three = db.Column(db.String(255))
    scrollers = db.relationship('Scroller', backref='defaulthaiku', lazy=True)

class Longmessage(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(1000))
    scroller = db.relationship('Scroller', backref='longmessage', uselist=False, lazy=True)

class Mood(db.Model, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    scrollers = db.relationship('Scroller', backref='mood', lazy=True)