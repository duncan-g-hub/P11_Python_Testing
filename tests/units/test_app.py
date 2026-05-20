def test_index_should_status_code_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_should_return_login_page(client):
    response = client.get('/')
    data = response.data.decode()
    assert 'Registration Portal' in data


def test_index_should_have_email_input(client):
    response = client.get('/')
    data = response.data.decode()
    assert 'type="email"' in data
