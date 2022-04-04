from app.extensions.database import db
from app.scrollers.models import Scroller

def test_scroller_update(client):
    # Updates scroller's properties
    scroller = Scroller(slug='test_for_update', to_recipient_name='rosie', from_sender_name='jim', defaulthaiku_id='1', mood_id='1')
    db.session.add(scroller)
    db.session.commit()

    scroller.to_recipient_name = 'maria'
    scroller.save()

    updated_scroller = Scroller.query.filter_by(slug='test_for_update').first()
    assert updated_scroller.to_recipient_name == 'maria'

def test_scroller_delete(client):
    # Deletes scroller
    scroller = Scroller(slug='test_for_del', to_recipient_name='jim', from_sender_name='rosie', defaulthaiku_id='1', mood_id='1')
    db.session.add(scroller)
    db.session.commit()

    scroller.delete()

    deleted_scroller = Scroller.query.filter_by(slug='test_for_del').first()
    assert deleted_scroller is None