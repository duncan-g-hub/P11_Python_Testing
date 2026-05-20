import pytest
import time
from selenium import webdriver

from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    # ouvre chrome avec le driver correspondant
    driver = webdriver.Chrome()
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
