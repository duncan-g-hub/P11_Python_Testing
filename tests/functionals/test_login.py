import pytest
import time
from selenium import webdriver

from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    # ouvre chrome avec le driver correspondant
    driver  = webdriver.Chrome()
    yield driver
    driver.quit()

def test_user_can_login_and_see_dashboard(browser, live_server_url, valid_email):
    browser.get(f"{live_server_url}/")
    browser.find_element(By.NAME, "email").send_keys(valid_email)
    browser.find_element(By.NAME, "email").submit()
    time.sleep(1)
    assert "Logout" in browser.page_source


def test_user_cannot_login_with_wrong_email(browser, live_server_url, invalid_email="test@test.com"):
    browser.get(f"{live_server_url}/")
    browser.find_element(By.NAME, "email").send_keys(invalid_email)
    browser.find_element(By.NAME, "email").submit()
    time.sleep(1)
    assert "You do not have access to booking." in browser.page_source

# from tests.conftest import client, valid_email
#
# def test_user_can_login_and_see_dashboard(client, valid_email):
#     response = client.get('/')
#     assert response.status_code == 200
#     assert 'Registration Portal' in response.data.decode()
#
#     response = client.post('/showSummary', data={'email': valid_email}, follow_redirects=True)
#     data = response.data.decode()
#
#     assert response.status_code == 200
#     assert 'Logout' in data
#
# def test_user_cannot_login_with_wrong_email(client, invalid_email="test@test.com"):
#     response = client.get('/')
#     assert response.status_code == 200
#
#     response = client.post('/showSummary', data={'email': invalid_email}, follow_redirects=True)
#     data = response.data.decode()
#
#     assert response.status_code == 200
#     assert "You do not have access to booking" in data