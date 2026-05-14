import pytest
import json
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_email():
    with open('clubs.json') as c:
        clubs = json.load(c)['clubs']
    return clubs[0]['email']