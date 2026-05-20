import html


def test_integration_book_then_purchase_places(client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = "4"

    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert 'How many places?' in response.data.decode()

    response = client.post('/purchase-places', data={
        'places': number_of_place,
        'competition_name': competition_name,
        'club_name': club_name
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.data.decode()

    assert int(valid_competition["number_of_places"]) == places_before - int(number_of_place)
    assert int(valid_club["points"]) == points_before - int(number_of_place)


def test_integration_book_then_purchase_places_with_too_many_places(client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = places_before + 1

    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200

    response = client.post('/purchase-places', data={
        'places': number_of_place,
        'competition_name': competition_name,
        'club_name': club_name
    })
    assert response.status_code == 200
    assert "You can't book this number of places" in html.unescape(response.data.decode())
    assert int(valid_competition["number_of_places"]) == places_before
    assert int(valid_club["points"]) == points_before
