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
    with client:
        # Create new user and log in
        client.post('/register', data=dict(email='test999@test.test', password='test', password_confirmation='test'))
        # Create new scroller while logged in
        client.post('/create', data={'to-recipient-name': 'lisa',
        'from-sender-name': ':)',
        'default-message': 'True',
        'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'mood': 'spring'})
        # Check scroller in index list
        response = client.get('/myscrollers', follow_redirects=True)
        assert b'lisa' in response.data
        # client.get('/logout')