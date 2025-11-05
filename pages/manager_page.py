import allure

from selenium.webdriver.common.alert import Alert
from .base_page import BasePage
from locators.locators import ManagerPageLocators
from data.values import ManagerPageValues
from page_factory.component import PageFactory
from helpers import closest_name_to_mean, PagesHelpers


class ManagerPageMain(BasePage):

    def click_add_customer_tab(self):
        with allure.step('CLick "Add Customer" tab'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_ADD_CUSTOMER).click()

    def click_customers_tab(self, timeout=10):
        with allure.step('CLick "Customers" tab'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_SHOW_CUSTOMERS).click()
            component.table(ManagerPageLocators.TABLE).click()


class ManagerPageAddCustomer(ManagerPageMain):

    def set_first_name(self):
        with allure.step('Set First Name in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_FIRST_NAME).set(ManagerPageValues.first_name())

    def set_last_name(self):
        with allure.step('Set Last Name in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_LAST_NAME).set(ManagerPageValues.last_name())

    def post_code_check(self):
        with allure.step('Post Code check'):
            assert ManagerPageValues.post_code().isdigit(), "Post code состоит не только из цифр"
            assert len(ManagerPageValues.post_code()) == 10, 'Длина Post code не соответствует необходимой'

    def set_post_code(self):
        with allure.step('Set Post Code in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_POST_CODE).set(ManagerPageValues.post_code())

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


class ManagerPageList(ManagerPageMain):

    def find_table_row_data(self):
        with allure.step('Find table row data by name in table'):
            row_data = PagesHelpers.find_row_by_column_value(self.browser, 0, ManagerPageValues.first_name())
            return row_data

    def find_customer_by_name(self):
        with allure.step('Find new added customer by name in table'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_SEARCH_CUSTOMER).set(ManagerPageValues.first_name())
            values = self.find_table_row_data().values()
            required_values = [ManagerPageValues.first_name(), ManagerPageValues.post_code(),
                               ManagerPageValues.last_name()]
            assert all(value in values for value in required_values), "Имя нового пользователя не найдено"

    def check_custom_user(self):
        with allure.step('Find new added customer by name in table'):
            assert ManagerPageValues.FIRST_NAME_SELF_CHECK == ManagerPageValues.FIRST_NAME_SPECIAL, \
                'Имя не соответствует правилам преобразования'

    def find_name_row_data(self):
        with allure.step('Delete customer by rules'):
            delete_name = closest_name_to_mean(PagesHelpers.get_all_first_names(self.browser))
            row_data = PagesHelpers.find_row_by_column_value(self.browser, 0, delete_name)
            return row_data

    def delete_customer(self):
        with allure.step('Delete customer by rules'):
            component = PageFactory(self.browser)
            delete_name = closest_name_to_mean(PagesHelpers.get_all_first_names(self.browser))
            row_data = self.find_name_row_data()
            component.input(ManagerPageLocators.INPUT_SEARCH_CUSTOMER).set(delete_name)
            component.button(ManagerPageLocators.BTN_DELETE_CUSTOMER).click()
            row_data2 = PagesHelpers.find_row_by_column_value(self.browser, 0, delete_name)
            assert row_data != row_data2, "Новый пользователь не удален"

    def set_first_name_sort_link(self):
        with allure.step('Click on sort by name link one time'):
            component = PageFactory(self.browser)
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()

    def check_first_name_sort_link(self):
        with allure.step('Click on sort by name link one time'):
            component = PageFactory(self.browser)
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()
            actual_sort_names = PagesHelpers.get_all_first_names(self.browser)
            assert actual_sort_names == sorted(actual_sort_names,
                                               reverse=True), 'Имена после первой сортировки расположены не по убыванию'
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()
            actual_sort_names = PagesHelpers.get_all_first_names(self.browser)
            assert actual_sort_names == sorted(
                actual_sort_names), 'Имена после второй сортировки расположены не по возрастанию'
