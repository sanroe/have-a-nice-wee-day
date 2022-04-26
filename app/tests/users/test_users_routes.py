def test_login_success(client):
    # Page loads
    response = client.get('/login')
    assert response.status_code == 200

def test_login_content(client):
    # Returns login content
    response = client.get('/login')
    assert b'<h1 class="text-center">login</h1>' in response.data

def test_register_success(client):
    # Page loads
    response = client.get('/register')
    assert response.status_code == 200

def test_register_content(client):
    # Returns register content
    response = client.get('/register')
    assert b'<h1 class="text-center">register</h1>' in response.data

def test_manage_redirects_if_not_logged_in(client):
    # Redirects if not logged in
    response = client.get('/manage')
    assert response.status_code == 302

def test_manage_unauthorised_loads_if_not_logged_in(client):
    # Unauthorised page loads if not logged in
    response = client.get('/manage', follow_redirects=True)
    assert 'unauthorised' in response.get_data(as_text=True)
