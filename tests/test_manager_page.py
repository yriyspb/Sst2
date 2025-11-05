import allure

from pages.manager_page import ManagerPageAddCustomer, ManagerPageList


@allure.feature('E2E manager page tests')
@allure.story('Проверка страницы добавления, просмотра и удаления клиентов')
@allure.severity('critical')
@allure.title("Тест самопроверки генерации имени согласно правилам")
def test_user_data_self_check(browser, manager_page):
    manager_page.click_add_customer_tab()
    add_customer_page = ManagerPageAddCustomer(browser, browser.current_url)
    add_customer_page.set_special_post_code()
    add_customer_page.set_first_name()
    add_customer_page.set_last_name()
    list_page = ManagerPageList(browser, browser.current_url)
    list_page.check_custom_user()


@allure.title("E2E тест создания клиента")
def test_add_user_success(browser, manager_page):
    manager_page.click_add_customer_tab()
    add_customer_page = ManagerPageAddCustomer(browser, browser.current_url)
    add_customer_page.set_first_name()
    add_customer_page.set_last_name()
    add_customer_page.post_code_check()
    add_customer_page.set_post_code()
    add_customer_page.click_add_customer_button()
    manager_page.click_customers_tab()
    list_page = ManagerPageList(browser, browser.current_url)
    list_page.find_customer_by_name()


@allure.title("E2E тест сортировки клиентов по имени (First Name)")
def test_sort_user_by_first_name(browser, manager_page):
    manager_page.click_add_customer_tab()
    add_customer_page = ManagerPageAddCustomer(browser, browser.current_url)
    add_customer_page.add_some_users()
    manager_page.click_customers_tab()
    list_page = ManagerPageList(browser, browser.current_url)
    list_page.check_first_name_sort_link()


@allure.title("E2E тест удаления клиента")
def test_delete_user_success(browser, manager_page):
    manager_page.click_add_customer_tab()
    add_customer_page = ManagerPageAddCustomer(browser, browser.current_url)
    add_customer_page.set_first_name()
    add_customer_page.set_last_name()
    add_customer_page.set_post_code()
    add_customer_page.click_add_customer_button()
    manager_page.click_customers_tab()
    list_page = ManagerPageList(browser, browser.current_url)
    list_page.delete_customer()
