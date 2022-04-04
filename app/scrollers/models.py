from app.extensions.database import db

class Scroller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    to_recipient_name = db.Column(db.String(80))
    long_message = db.Column(db.String(65535))
    from_sender_name = db.Column(db.String(80))