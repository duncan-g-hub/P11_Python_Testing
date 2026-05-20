import html  # pour .unescape() -> permet de ne pas echapper les apostrophes issues du html


def test_book_should_return_booking_page_with_valid_competiton_and_club(client, valid_competition, valid_club):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert competition_name in response.data.decode()
    assert 'How many places?' in response.data.decode()


def test_book_should_return_welcome_page_with_invalid_competition_and_valid_club(client, valid_club):
    competition_name = "invalide_competition_name"
    club_name = valid_club["name"]
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()


def test_book_should_redirect_index_with_invalid_club_and_valid_competition(client, valid_competition):
    competition_name = valid_competition["name"]
    club_name = "invalid_club_name"
    response = client.get(f'/book/{competition_name}/{club_name}', follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration Portal' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()


def test_book_should_redirect_index_with_invalid_club_and_competition(client):
    competition_name = "invalide_competition_name"
    club_name = "invalid_club_name"
    response = client.get(f'/book/{competition_name}/{club_name}', follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration Portal' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()


def test_purchase_places_should_return_welcome_page_with_valid_competiton_and_club(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    number_of_place = "4"
    response = client.post('/purchase-places', data={'places': number_of_place,
                                                     'competition_name': competition_name,
                                                     'club_name': club_name})
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode()
    assert 'Great-booking complete!' in response.data.decode()


def test_purchase_places_should_return_welcome_page_with_invalid_competiton_and_valid_club(
        client, valid_club):
    competition_name = "invalid_competition_name"
    club_name = valid_club["name"]
    number_of_place = "4"
    response = client.post('/purchase-places', data={'places': number_of_place,
                                                     'competition_name': competition_name,
                                                     'club_name': club_name})
    assert response.status_code == 200
    assert 'Welcome' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()


def test_purchase_places_should_redirect_index_page_with_valid_competiton_and_invalid_club(
        client, valid_competition):
    competition_name = valid_competition["name"]
    club_name = "invalid_club_name"
    number_of_place = "4"
    response = client.post('/purchase-places',
                           data={'places': number_of_place,
                                 'competition_name': competition_name,
                                 'club_name': club_name},
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration Portal' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()


def test_purchase_places_should_redirect_index_page_with_invalid_competiton_and_club(client):
    competition_name = "invalid_competition_name"
    club_name = "invalid_club_name"
    number_of_place = "4"
    response = client.post('/purchase-places',
                           data={'places': number_of_place,
                                 'competition_name': competition_name,
                                 'club_name': club_name},
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration Portal' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()


def test_purchase_places_should_deduct_places_and_points_with_valid_competition_and_club(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = "4"
    client.post('/purchase-places', data={'places': number_of_place,
                                          'competition_name': competition_name,
                                          'club_name': club_name})
    assert int(valid_competition["number_of_places"]) == places_before - int(number_of_place)
    assert int(valid_club["points"]) == points_before - int(number_of_place)


def test_purchase_places_should_not_deduct_places_and_points_with_invalid_competition_and_club(
        client, valid_club, valid_competition):
    competition_name = "invalid_competition_name"
    club_name = "invalid_club_name"
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = "4"
    client.post('/purchase-places', data={'places': number_of_place,
                                          'competition_name': competition_name,
                                          'club_name': club_name})
    assert int(valid_competition["number_of_places"]) == places_before
    assert int(valid_club["points"]) == points_before


def test_purchase_places_should_not_deduct_places_and_points_with_invalid_competition_and_valid_club(
        client, valid_club, valid_competition):
    competition_name = "invalid_competition_name"
    club_name = valid_club["name"]
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = "4"
    client.post('/purchase-places', data={'places': number_of_place,
                                          'competition_name': competition_name,
                                          'club_name': club_name})
    assert int(valid_competition["number_of_places"]) == places_before
    assert int(valid_club["points"]) == points_before


def test_purchase_places_should_not_deduct_places_and_points_with_valid_competition_and_invalid_club(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = "invalid_club_name"
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = "4"
    client.post('/purchase-places', data={'places': number_of_place,
                                          'competition_name': competition_name,
                                          'club_name': club_name})
    assert int(valid_competition["number_of_places"]) == places_before
    assert int(valid_club["points"]) == points_before


def test_purchase_places_should_not_work_with_nb_booked_places_superior_than_nb_competition_places(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    comp_places = int(valid_competition["number_of_places"])
    number_of_place = comp_places + 1
    response = client.post('/purchase-places', data={'places': number_of_place,
                                                     'competition_name': competition_name,
                                                     'club_name': club_name})
    assert (f"You can't book this number of places. This competition have {comp_places} places remaining."
            in html.unescape(response.data.decode()))  # permet de ne pas echapper les apostrophes issues du html


def test_purchase_places_should_not_work_with_nb_booked_places_superior_than_nb_club_points(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    club_points = int(valid_club["points"])
    number_of_place = club_points + 1
    response = client.post('/purchase-places', data={'places': number_of_place,
                                                     'competition_name': competition_name,
                                                     'club_name': club_name})
    assert (f"You can't book this number of places with your club points. You have {club_points} points."
            in html.unescape(response.data.decode()))


def test_purchase_places_should_not_work_with_nb_booked_places_superior_than_12(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    number_of_place = 13
    response = client.post('/purchase-places', data={'places': number_of_place,
                                                     'competition_name': competition_name,
                                                     'club_name': club_name})
    assert ("You can't book more than 12 number of places"
            in html.unescape(response.data.decode()))


def test_purchase_places_should_not_work_with_negative_nb_booked_places(
        client, valid_club, valid_competition):
    competition_name = valid_competition["name"]
    club_name = valid_club["name"]
    number_of_place = -1
    response = client.post('/purchase-places', data={'places': number_of_place,
                                                     'competition_name': competition_name,
                                                     'club_name': club_name})
    assert ("You can't book a negative number of places"
            in html.unescape(response.data.decode()))
