import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from .base_page import BasePage
from ..locators.locators import ManagerPageLocators
from ..data.values import ManagerPageValues
from ..page_factory.component import PageFactory
from ..helpers import closest_name_to_mean, get_all_first_names, find_row_by_column_value


class ManagerPage(BasePage):

    def click_add_customer_tab(self):
        with allure.step('CLick "Add Customer" tab'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_ADD_CUSTOMER).click()

    def set_first_name(self):
        with allure.step('Set First Name in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_FIRST_NAME).set(ManagerPageValues.FIRST_NAME)

    def set_last_name(self):
        with allure.step('Set Last Name in input'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_LAST_NAME).set(ManagerPageValues.LAST_NAME)

    def set_post_code(self):
        with allure.step('Set Post Code in input'):
            component = PageFactory(self.browser)
            assert len(ManagerPageValues.POST_CODE) == 10, 'Длина Post code не соответствует необходимой'
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

    def click_customers_tab(self, timeout=10):
        with allure.step('CLick "Customers" tab'):
            component = PageFactory(self.browser)
            component.button(ManagerPageLocators.BTN_SHOW_CUSTOMERS).click()
            try:
                WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_element_located(ManagerPageLocators.TABLE)
                )
                print("Страница успешно загрузилась")
                return True
            except Exception as e:
                print(f"Страница не загрузилась: {e}")
                return False

    def find_customer_by_name(self):
        with allure.step('Find new added customer by name in table'):
            component = PageFactory(self.browser)
            component.input(ManagerPageLocators.INPUT_SEARCH_CUSTOMER).set(ManagerPageValues.FIRST_NAME)
            row_data = find_row_by_column_value(self.browser, 0, ManagerPageValues.FIRST_NAME)
            required_values = [ManagerPageValues.FIRST_NAME, ManagerPageValues.POST_CODE, ManagerPageValues.LAST_NAME]
            assert all(value in row_data.values() for value in required_values), "Имя нового пользователя не найдено"

    def check_custom_user(self):
        with allure.step('Find new added customer by name in table'):
            assert ManagerPageValues.FIRST_NAME_SELF_CHECK == ManagerPageValues.FIRST_NAME_SPECIAL, \
                'Имя не соответствует правилам преобразования'

    def delete_customer(self):
        with allure.step('Delete customer by rules'):
            component = PageFactory(self.browser)
            delete_name = closest_name_to_mean(get_all_first_names(self.browser))
            row_data = find_row_by_column_value(self.browser, 0, delete_name)
            print(row_data)
            component.input(ManagerPageLocators.INPUT_SEARCH_CUSTOMER).set(delete_name)
            component.button(ManagerPageLocators.BTN_DELETE_CUSTOMER).click()
            row_data2 = find_row_by_column_value(self.browser, 0, delete_name)
            print(row_data2)
            assert row_data != row_data2, "Новый пользователь не удален"

    def set_first_name_sort_link(self):
        with allure.step('Click on sort by name link one time'):
            component = PageFactory(self.browser)
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()

    def check_first_name_sort_link(self):
        with allure.step('Click on sort by name link one time'):
            component = PageFactory(self.browser)
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()
            actual_sort_names = get_all_first_names(self.browser)
            assert actual_sort_names == sorted(actual_sort_names,
                                               reverse=True), 'Имена после первой сортировки расположены не по убыванию'
            component.link(ManagerPageLocators.LINK_SORT_BY_FIRST_NAME).click()
            actual_sort_names = get_all_first_names(self.browser)
            assert actual_sort_names == sorted(
                actual_sort_names), 'Имена после второй сортировки расположены не по возрастанию'
