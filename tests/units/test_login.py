from tests.conftest import client, valid_email


def test_should_login_with_correct_email_and_status_code_200(client, valid_email):
    response = client.post('/showSummary', data={'email': valid_email})
    assert response.status_code == 200
    data = response.data.decode()
    assert 'Logout' in data

def test_should_not_login_with_empty_email(client):
    response = client.post('/showSummary', data={'email': ''})
    data = response.data.decode()
    assert "You do not have access to booking" in data

def test_should_not_login_with_wrong_email(client):
    response = client.post('/showSummary', data={'email': "test@test.com"})
    data = response.data.decode()
    assert "You do not have access to booking" in data

def test_welcome_page_should_display_competitions(client, valid_email):
    response = client.post('/showSummary', data={'email': valid_email})
    data = response.data.decode()
    assert 'competitions' in data.lower()