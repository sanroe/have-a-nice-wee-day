from app.extensions.database import db
from app.users.models import User

def test_login_success(client):
    # Page loads
    response = client.get('/login')
    assert response.status_code == 200

def test_login_content(client):
    # Returns login content
    response = client.get('/login')
    assert b'<h1 class="text-center">login</h1>' in response.data

def test_login_user_exists_post(client):
    # Logins in user
    # Create fake user first
    user = User(email='test_for_login@test.test', password='test')
    db.session.add(user)
    db.session.commit()
    response = client.post('/login', data=dict(email='test_for_login@test.test', password='test'), follow_redirects=True)
    assert b'your scrollers' in response.data

def  test_login_user_does_not_exist_post(client):
    # Throws error if user does not exist
    response = client.post('/login', data=dict(email='xyz@test.test', password='test'), follow_redirects=True)
    assert b'no user with that email address found' in response.data

def test_login_user_exists_wrong_password_post(client):
    # Throws error if user exists but password is wrong
    # Create fake user first
    user = User(email='test7@test.test', password='test')
    db.session.add(user)
    db.session.commit()
    response = client.post('/login', data=dict(email='test7@test.test', password='wrong'), follow_redirects=True)
    assert b'password is incorrect' in response.data

def test_register_success(client):
    # Page loads
    response = client.get('/register')
    assert response.status_code == 200

def test_register_content(client):
    # Returns register content
    response = client.get('/register')
    assert b'<h1 class="text-center">register</h1>' in response.data

def test_register_post(client):
    # Creates a user record
    client.post('/register', data=dict(email='testregister@test.test', password='test', password_confirmation='test'))
    client.get('/logout')
    assert User.query.filter_by(email='testregister@test.test').first() is not None

def test_manage_redirects_if_not_logged_in(client):
    # Redirects if not logged in
    response = client.get('/manage')
    assert response.status_code == 302

def test_manage_unauthorised_loads_if_not_logged_in(client):
    # Unauthorised page loads if not logged in
    response = client.get('/manage', follow_redirects=True)
    assert 'unauthorised' in response.get_data(as_text=True)

def test_manage_logged_in_success(client):
    # Page loads if logged in
    # Create fake user
    user = User(email='test@test.test', password='test')
    db.session.add(user)
    db.session.commit()
    with client:
        client.post('/login', data=dict(email='test@test.test', password='test'), follow_redirects=True)
        response = client.get('/manage')
        assert response.status_code == 200

def test_manage_logged_in_content(client):
    # Returns if logged in
    # Create fake user and log in
    user = User(email='testing@test.test', password='testing')
    db.session.add(user)
    db.session.commit()
    with client:
        client.post('/login', data=dict(email='testing@test.test', password='testing'), follow_redirects=True)
        response = client.get('/manage')
        assert 'update email' in response.get_data(as_text=True)