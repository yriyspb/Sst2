from selenium.webdriver.common.by import By


class ManagerPageLocators():
    BTN_ADD_CUSTOMER = (By.CSS_SELECTOR, "button[ng-click='addCust()']")
    BTN_SHOW_CUSTOMERS = (By.CSS_SELECTOR, "button[ng-click='showCust()']")
    LINK_SORT_BY_FIRST_NAME = (By.LINK_TEXT, "First Name")
    INPUT_FIRST_NAME = (By.CSS_SELECTOR, "input[ng-model='fName']")
    INPUT_LAST_NAME = (By.CSS_SELECTOR, "input[ng-model='lName']")
    INPUT_POST_CODE = (By.CSS_SELECTOR, "input[ng-model='postCd']")
    BTN_ADD_SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    BTN_DELETE_CUSTOMER = (By.CSS_SELECTOR, "button[ng-click='deleteCust(cust)']")
    INPUT_SEARCH_CUSTOMER = (By.CSS_SELECTOR, "input[ng-model='searchCustomer']")
    TABLE = (By.CSS_SELECTOR, "table.table tbody tr")
