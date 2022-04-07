def test_view_success(client):
    # Page loads
    response = client.get('/view/<slug>')
    assert response.status_code == 200

def test_view_content(client):
    # Returns scroller view content
    response = client.get('/view/<slug>')
    assert b"<title>the uplifting scroller project &ndash; view</title>" in response.data

def test_create_success(client):
    # Page loads
    response = client.get('/create')
    assert response.status_code == 200

def test_create_content(client):
    # Returns create content
    response = client.get('/create')
    assert 'whose day are we making?' in response.get_data(as_text=True)

def test_404_redirect(client):
    # Nonexistent page redirects
    response = client.get('/asdfejioj')
    assert response.status_code == 302

def test_404_success(client):
    # Page loads
    response = client.get('/404')
    assert response.status_code == 200

def test_404_content(client):
    # Returns 404 content
    response = client.get('/404')
    assert 'Page not found' in response.get_data(as_text=True)