def test_integration_purchase_places_then_clubs_table(client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    points_before = int(valid_club["points"])
    number_of_place = "4"

    response = client.post('/purchase-places', data={
        'places': number_of_place,
        'competition_name': competition_name,
        'club_name': club_name
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode()

    response = client.get('/clubs-table')
    assert response.status_code == 200
    assert club_name in response.data.decode()
    assert f"Points : {points_before - int(number_of_place)}" in response.data.decode()
