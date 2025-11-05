import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.manager_page import ManagerPageMain
from data.values import ManagerPageValues


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
    page = ManagerPageMain(browser, ManagerPageValues.LINK)
    page.open()
    return page
