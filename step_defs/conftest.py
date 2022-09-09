import pytest
from selenium import webdriver
from .settings import console_logger

@pytest.fixture(scope="function")
def browser():
    try:
        console_logger.debug('Start browser')
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.implicitly_wait(10)
        yield browser
        console_logger.debug('Quit browser')
        browser.quit()
    except:
        console_logger.exception('Something wrong this browser fixture')


class ValueStorage:
    remembered_phone = None
    remembered_phone_rating = None
