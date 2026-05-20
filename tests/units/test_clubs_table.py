from tests.conftest import client, valid_club

def test_clubs_table_should_return_status_code_200(client):
    response = client.get('/clubs-table')
    assert response.status_code == 200

def test_clubs_table_should_return_clubs_table_page(client):
    response = client.get('/clubs-table')
    assert "Clubs Table :" in response.data.decode()

def test_clubs_table_should_return_clubs_and_points(client, valid_club):
    response = client.get('/clubs-table')
    assert valid_club["name"] in response.data.decode()
    assert f"Points : {valid_club["points"]}" in response.data.decode()
