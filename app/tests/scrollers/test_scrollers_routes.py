from app.extensions.database import db
from app.scrollers.models import Scroller
from app.users.models import User

def test_view_success(client):
    # Page loads if scroller exists
    scroller = Scroller(slug='test_for_view')
    db.session.add(scroller)
    db.session.commit()
    response = client.get('/view/test_for_view')
    assert response.status_code == 200

def test_view_content(client):
    # Returns scroller view content if exists
    response = client.get('/view/<slug>')
    if response == 200:
        assert b"<title>the uplifting scroller project &ndash; view</title>" in response.data

def test_get_create_success(client):
    # Page loads
    response = client.get('/create')
    assert response.status_code == 200

def test_get_create_content(client):
    # Returns create content
    response = client.get('/create')
    assert 'whose day are we making?' in response.get_data(as_text=True)

def test_post_create_scroller(client):
    # Creates a scroller record
    response = client.post('/create', data={
        'to-recipient-name': 'diana',
        'from-sender-name': ':)',
        'default-message': 'True',
        'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'mood': 'spring'
    })
    assert Scroller.query.first() is not None

def test_myscrollers_renders_scrollers(client):
    # Page loads and renders scrollers
    # Creat fake user and log in
    user = User(email='test2@test.test', password='test2')
    db.session.add(user)
    db.session.commit()
    with client:
        client.post('/login', data=dict(email='test2@test.test', password='test2'), follow_redirects=True)
        # Create new scroller and assign user
        new_scroller = Scroller(slug='test-for-list', to_recipient_name='lisa', user_id=user.id)
        new_scroller.save()
        db.session.add(new_scroller)
        db.session.commit()
        # Check saved scroller appears in list
        response = client.get('/myscrollers')
        assert b'lisa' in response.data