def test_index_success(client):
    # Page loads
    response = client.get('/')
    assert response.status_code == 200

def test_index_content(client):
    # Returns landing text
    response = client.get('/')
    assert b'day...' in response.data

def test_about_success(client):
    # Page loads
    response = client.get('/about')
    assert response.status_code == 200

def test_about_content(client):
    # Returns about text
    response = client.get('/about')
    assert 'philosophy' in response.get_data(as_text=True)

def test_legal_success(client):
    # Page loads
    response = client.get('/legal')
    assert response.status_code == 200

def test_legal_content(client):
    # Returns legal text
    response = client.get('/legal')
    assert 'disclaimer' in response.get_data(as_text=True)

def test_404_success(client):
    # Page loads
    response = client.get('/404')
    assert response.status_code == 200

def test_404_content(client):
    # Returns 404 content
    response = client.get('/404')
    assert 'page not found' in response.get_data(as_text=True)

def test_404_redirect(client):
    # Nonexistent page redirects
    response = client.get('/asdfejioj')
    assert response.status_code == 302