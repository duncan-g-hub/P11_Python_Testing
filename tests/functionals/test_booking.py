import pytest
import time
from selenium import webdriver

from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    driver  = webdriver.Chrome()
    yield driver
    driver.quit()

def test_user_can_book_places_on_competition(browser, live_server_url, valid_email, valid_club, valid_competition):
    places_before = int(valid_competition["number_of_places"])
    points_before = int(valid_club["points"])
    number_of_place = "4"

    browser.get(f"{live_server_url}/")
    browser.find_element(By.NAME, "email").send_keys(valid_email)
    browser.find_element(By.NAME, "email").submit()
    time.sleep(1)

    browser.find_element(By.LINK_TEXT, "Book Places").click()
    time.sleep(1)

    browser.find_element(By.NAME, "places").send_keys(number_of_place)
    browser.find_element(By.NAME, "places").submit()
    time.sleep(1)

    assert "Welcome" in browser.page_source
    assert "Great-booking complete!" in browser.page_source
    assert int(valid_competition["number_of_places"]) == places_before - int(number_of_place)
    assert int(valid_club["points"]) == points_before - int(number_of_place)
