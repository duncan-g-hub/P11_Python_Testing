import pytest
import time
from selenium import webdriver

from selenium.webdriver.common.by import By


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_user_can_logout(browser, live_server_url, valid_email):
    browser.get(f"{live_server_url}/")
    browser.find_element(By.NAME, "email").send_keys(valid_email)
    browser.find_element(By.NAME, "email").submit()
    time.sleep(1)
    browser.find_element(By.LINK_TEXT, "Logout").click()
    time.sleep(1)
    assert "Registration Portal" in browser.page_source
