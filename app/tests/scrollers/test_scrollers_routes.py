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
        'to-recipient-name': 'diana-diana',
        'from-sender-name': ':)',
        'default-message': 'True',
        'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'mood': 'spring'
    })
    assert Scroller.query.filter_by(to_recipient_name='diana-diana').first() is not None

def test_scroller_creation_success(client):
    # Page returns correct content
    response = client.post('/create', data={
        'to-recipient-name': 'banana',
        'from-sender-name': ':)',
        'default-message': 'True',
        'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'mood': 'spring'
    }, follow_redirects=True)
    # Check success page loaded
    assert b'success!' in response.data
    # Check correct slug is created and included
    assert b'banana-' in response.data

def test_scroller_creation_login_success(client):
    # Page returns correct content
    client.post('/create', data={
        'to-recipient-name': 'apple',
        'from-sender-name': ':)',
        'default-message': 'True',
        'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'mood': 'spring'
    }, follow_redirects=True)
    response = client.get('/success/login')
    # Check loaded
    assert response.status_code == 200
    # Check for login button included
    assert b'name="submit_button" value="login"' in response.data

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

def test_myscroller_delete(client):
    # Deletes scroller
    # Create new user and log in
    with client:
        client.post('/register', data=dict(email='test555@test.test', password='test', password_confirmation='test'))
        # Create new scroller while logged in
        client.post('/create', data={'to-recipient-name': 'cherry-top',
        'from-sender-name': ':)',
        'default-message': 'True',
        'long-message': 'lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'mood': 'spring'})
        scroller = Scroller.query.filter_by(to_recipient_name='cherry-top').first()
        scroller_slug = scroller.slug
        # Create delete URL to test
        del_url = '/delete/' + scroller_slug
        response = client.get(del_url, follow_redirects=True)
        assert Scroller.query.filter_by(to_recipient_name='cherry-top').first() is None
