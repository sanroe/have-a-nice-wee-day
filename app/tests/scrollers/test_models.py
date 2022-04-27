from app.extensions.database import db
from app.scrollers.models import Scroller, Customhaiku, Longmessage

# Tests for updating and deleting editable models (default haiku and mood are not editable)

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

def test_customhaiku_update(client):
    # Updates custom haiku properties
    customhaiku = Customhaiku(line_one='test', line_two='testing', line_three='tested')
    db.session.add(customhaiku)
    db.session.commit()

    customhaiku_id = customhaiku.id

    customhaiku.line_one = 'different'
    customhaiku.save()

    updated_customhaiku = Customhaiku.query.filter_by(id=customhaiku_id).first()
    assert updated_customhaiku.line_one == 'different'

def test_customhaiku_delete(client):
    # Deletes custom haiku
    customhaiku = Customhaiku(line_one='test', line_two='testing', line_three='tested')
    db.session.add(customhaiku)
    db.session.commit()

    customhaiku_id = customhaiku.id

    customhaiku.delete()

    deleted_customhaiku = Customhaiku.query.filter_by(id=customhaiku_id).first()
    assert deleted_customhaiku is None

def test_longmessage_update(client):
    # Updates long message properties
    longmessage = Longmessage(msg='lorem ipsum')
    db.session.add(longmessage)
    db.session.commit()

    longmessage_id = longmessage.id

    longmessage.msg = 'dolor sit amet'
    longmessage.save()

    updated_longmessage = Longmessage.query.filter_by(id=longmessage_id).first()
    assert updated_longmessage.msg == 'dolor sit amet'

def test_longmessage_delete(client):
    # Deletes long message
    longmessage = Longmessage(msg='lorem ipsum')
    db.session.add(longmessage)
    db.session.commit()

    longmessage_id = longmessage.id

    longmessage.delete()

    deleted_longmessage = Longmessage.query.filter_by(id=longmessage_id).first()
    assert deleted_longmessage is None