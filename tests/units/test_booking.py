from tests.conftest import client, valid_club, valid_competition


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
    assert 'Welcome'  in response.data.decode()
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
    response = client.post(f'/purchase-places', data={'places': number_of_place,
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
    response = client.post(f'/purchase-places', data={'places': number_of_place,
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
    response = client.post(f'/purchase-places',
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
    response = client.post(f'/purchase-places',
                           data={'places': number_of_place,
                                 'competition_name': competition_name,
                                 'club_name': club_name},
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration Portal' in response.data.decode()
    assert 'Something went wrong-please try again' in response.data.decode()




# consommation des points du club lors de la reservation
# pas de consommation des points si mauvais club ou mauvaise competition

# consommation du nombre de places dispo sur la competition lors de la reservation
# pas de consommation des places si mauvais club ou competition







# le nombre de places reservées ne peut pas etre superieure aux nombres de places de la competition
# le nombre de places reservées ne peut pas etre superieure aux nombres de points du club
# le nombre de places reservées ne peut pas etre superieure à 12