from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class BaseElement:
    def __init__(self, driver: WebDriver, locator: tuple, timeout: int = 10):
        self.driver = driver
        self.locator = locator
        self.timeout = timeout

    def find(self):
        wait = WebDriverWait(self.driver, self.timeout)
        return wait.until(EC.visibility_of_element_located(self.locator))


class InputElement(BaseElement):
    def set(self, value: str):
        el = self.find()
        el.clear()
        el.send_keys(value)
        return el


class TextAreaElement(InputElement):
    pass


class CheckboxElement(BaseElement):
    def check(self):
        el = self.find()
        if not el.is_selected():
            el.click()
        return el

    def uncheck(self):
        el = self.find()
        if el.is_selected():
            el.click()
        return el

    def toggle(self):
        el = self.find()
        el.click()
        return el


class SelectElement(BaseElement):
    def select_by_index(self, index: int):
        el = self.find()
        Select(el).select_by_index(index)
        return el

    def select_by_value(self, value: str):
        el = self.find()
        Select(el).select_by_value(value)
        return el

    def select_by_visible_text(self, text: str):
        el = self.find()
        Select(el).select_by_visible_text(text)
        return el


class ButtonElement(BaseElement):
    def click(self):
        el = self.find()
        el.click()
        return el

class LinkElement(BaseElement):
    def click(self):
        el = self.find()
        el.click()
        return el

class PageFactory:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def input(self, locator: tuple) -> InputElement:
        return InputElement(self.driver, locator)

    def textarea(self, locator: tuple) -> TextAreaElement:
        return TextAreaElement(self.driver, locator)

    def checkbox(self, locator: tuple) -> CheckboxElement:
        return CheckboxElement(self.driver, locator)

    def select(self, locator: tuple) -> SelectElement:
        return SelectElement(self.driver, locator)

    def button(self, locator: tuple) -> ButtonElement:
        return ButtonElement(self.driver, locator)

    def link(self, locator: tuple) -> LinkElement:
        return LinkElement(self.driver, locator)
