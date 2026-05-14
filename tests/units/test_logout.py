from tests.conftest import client

def test_logout_should_redirect(client):
    response = client.get('/logout')
    assert response.status_code == 302

def test_logout_should_redirect_to_index(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    data = response.data.decode()
    assert 'Registration Portal' in data