import allure

@allure.feature('E2E manager page tests')
@allure.story('Проверка страницы добавления, просмотра и удаления клиентов')
@allure.severity('critical')
def test_user_data_self_check(browser, manager_page):
    manager_page.click_add_customer_tab()
    manager_page.set_special_post_code()
    manager_page.set_first_name()
    manager_page.set_last_name()
    manager_page.check_custom_user()


def test_add_user_success(browser, manager_page):
    manager_page.click_add_customer_tab()
    manager_page.set_first_name()
    manager_page.set_last_name()
    manager_page.set_post_code()
    manager_page.click_add_customer_button()
    manager_page.click_customers_tab()
    manager_page.find_customer_by_name()


def test_sort_user_by_first_name(browser, manager_page):
    manager_page.click_add_customer_tab()
    for i in range(4):
        manager_page.set_first_name()
        manager_page.set_last_name()
        manager_page.set_post_code()
        manager_page.click_add_customer_button()
    manager_page.click_customers_tab()
    manager_page.check_first_name_sort_link()


def test_delete_user_success(browser, manager_page):
    manager_page.click_add_customer_tab()
    manager_page.set_first_name()
    manager_page.set_last_name()
    manager_page.set_post_code()
    manager_page.click_add_customer_button()
    manager_page.click_customers_tab()
    manager_page.delete_customer()
