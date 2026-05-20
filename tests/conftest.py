import pytest
import threading

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_email():
    import server
    server.clubs = server.load_clubs()
    return server.clubs[0]["email"]


@pytest.fixture
def valid_club():
    import server
    server.clubs = server.load_clubs()
    return server.clubs[0]


@pytest.fixture
def valid_competition():
    import server
    server.competitions = server.load_competitions()
    return server.competitions[0]


@pytest.fixture(scope="session")  # fixture créée qu'une seule fois pour toute la session de tests
def live_server_url():
    # Crée un thread séparé qui va exécuter app.run()
    thread = threading.Thread(target=lambda: app.run(port=5001, use_reloader=False))
    # thread s'arrêtera automatiquement quand le programme principal (pytest) se termine
    thread.daemon = True
    # démarre le serveur Flask
    thread.start()
    # yield à la place de return permet à pytest de récupérer l'URL et de continuer à exécuter les tests
    yield "http://127.0.0.1:5001"
