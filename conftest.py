import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.manager_page import PageMain
from data.values import ManagerPageValues
from helpers.api_client import ApiClient


@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--incognito")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture
def manager_page(browser):
    page = PageMain(browser, ManagerPageValues.LINK)
    page.open()
    return page


@pytest.fixture
def create_entity():
    test_suite = ApiClient()
    entity_id = test_suite.create_test_entity()
    yield entity_id
    test_suite.cleanup_entity(entity_id)