import allure

from selenium.webdriver.common.alert import Alert
from .base_page import BasePage
from locators.locators import ManagerPageLocators
from data.values import ManagerPageValues
from page_factory.component import PageFactory
from helpers import closest_name_to_mean, generate_post_code, post_code_to_first_name
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class PageMain(BasePage):

    def click_add_customer_tab(self):
        with allure.step('CLick "Add Customer" tab'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_ADD_CUSTOMER).click()

    def click_customers_tab(self, timeout=10):
        with allure.step('CLick "Customers" tab'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_SHOW_CUSTOMERS).click()
            component.table(ManagerPageLocators.TABLE).click()


class PageFunctions(BasePage):

    def get_all_first_names(self):
        soup = BeautifulSoup(self.page_source, "html.parser")

        table = soup.find("table", {"class": "table table-bordered table-striped"})

        header = table.find("tr")
        headers = [th.get_text(strip=True) for th in header.find_all(["th", "td"])]
        first_name_col_index = headers.index("First Name")

        values = []
        for row in table.find_all("tr")[1:]:
            cells = row.find_all(["td", "th"])
            if len(cells) > first_name_col_index:
                values.append(cells[first_name_col_index].get_text(strip=True))
        return values

    def find_row_by_column_value(self, search_column_index, search_value):
        rows = self.find_elements(By.CSS_SELECTOR, "table tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > search_column_index:
                if cells[search_column_index].text == search_value:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        row_data[i] = cell.text
                    return row_data
        return None


class PageAddCustomer(PageMain):

    def set_first_name(self):
        with allure.step('Set First Name in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_FIRST_NAME).set(ManagerPageValues.FIRST_NAME)

    def set_last_name(self):
        with allure.step('Set Last Name in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_LAST_NAME).set(ManagerPageValues.LAST_NAME)

    def post_code_check(self):
        with allure.step('Set Post Code in input'):
            assert len(ManagerPageValues.POST_CODE) == 10, 'Длина Post code не соответствует необходимой'

    def set_post_code(self):
        with allure.step('Set Post Code in input'):
            component = PageFactory(self.browser)
            assert ManagerPageValues.POST_CODE.isdigit(), "Post code состоит не только из цифр"
            component.input(ManagerPageLocators.INPUT_POST_CODE).set(ManagerPageValues.POST_CODE)

    def set_special_post_code(self):
        with allure.step('Set self-check Post Code in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_POST_CODE).set(ManagerPageValues.POST_CODE_SPECIAL)

    def click_add_customer_button(self):
        with allure.step('CLick "Add Customer" button'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_ADD_SUBMIT).click()
            alert = Alert(self.browser)
            alert.accept()

    def add_some_users(self):
        with allure.step('Добавить сразу несколько новых пользователей'):
            for i in range(4):
                self.set_post_code()
                self.set_first_name()
                self.set_last_name()
                self.click_add_customer_button()
                ManagerPageValues.POST_CODE = generate_post_code()
                ManagerPageValues.FIRST_NAME = post_code_to_first_name(ManagerPageValues.POST_CODE)


class PageList(PageMain):

    def find_table_row_data(self):
        with allure.step('Find table row data by name in table'):
            row_data = PageFunctions.find_row_by_column_value(self.browser, 0, ManagerPageValues.FIRST_NAME)
            return row_data

    def set_customer_name_to_search(self):
        with allure.step('Set customer name to search input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_SEARCH_CUSTOMER).set(ManagerPageValues.FIRST_NAME)

    def check_customer_by_name(self):
        with allure.step('Check customer data in table'):
            values = self.find_table_row_data().values()
            required_values = [ManagerPageValues.FIRST_NAME, ManagerPageValues.POST_CODE, ManagerPageValues.LAST_NAME]
            assert all(value in values for value in required_values), "Имя нового пользователя не найдено"

    def check_custom_user(self):
        with allure.step('Find new added customer by name in table'):
            assert ManagerPageValues.FIRST_NAME_SELF_CHECK == ManagerPageValues.FIRST_NAME_SPECIAL, \
                'Имя не соответствует правилам преобразования'

    def find_name_row_data(self):
        with allure.step('Delete customer by rules'):
            delete_name = closest_name_to_mean(PageFunctions.get_all_first_names(self.browser))
            row_data = PageFunctions.find_row_by_column_value(self.browser, 0, delete_name)
            return row_data

    def set_customer_name_for_delete(self):
        with allure.step('Set customer name for delete to search input'):
            delete_name = closest_name_to_mean(PageFunctions.get_all_first_names(self.browser))
        return delete_name

    def set_customer_name_for_delete_to_search(self, delete_name):
        with allure.step('Set customer name for delete to search input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_SEARCH_CUSTOMER).set(delete_name)
        return delete_name

    def execute_customer_delete(self):
        with allure.step('Delete customer execute'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_DELETE_CUSTOMER).click()

    def check_customer_after_delete(self, delete_name, original_row_data):
        with allure.step('Check customer data after delete'):
            row_data_after_delete = PageFunctions.find_row_by_column_value(self.browser, 0, delete_name)
            assert original_row_data != row_data_after_delete, "Новый пользователь не удален"
            return row_data_after_delete

    def delete_customer(self):
        with (allure.step('Delete customer by rules')):
            original_row_data = self.find_name_row_data()
            delete_name = self.set_customer_name_for_delete()
            self.set_customer_name_for_delete_to_search(delete_name)
            self.execute_customer_delete()
            self.check_customer_after_delete(delete_name, original_row_data)

    def set_first_name_sort_link(self):
        with allure.step('Click on sort by name link one time'):
            component = PageFactory(self.browser)
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()

    def check_first_name_sort_link(self):
        with allure.step('Click on sort by name link one time'):
            component = PageFactory(self.browser)
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()
            actual_sort_names = PageFunctions.get_all_first_names(self.browser)
            assert actual_sort_names == sorted(actual_sort_names,
                                               reverse=True), 'Имена после первой сортировки расположены не по убыванию'
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()
            actual_sort_names = PageFunctions.get_all_first_names(self.browser)
            assert actual_sort_names == sorted(
                actual_sort_names), 'Имена после второй сортировки расположены не по возрастанию'
