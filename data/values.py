from helpers import generate_post_code, post_code_to_first_name
from faker import Faker

faker = Faker()


class ManagerPageValues():
    LINK = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager"
    POST_CODE = generate_post_code()
    POST_CODE_SPECIAL = "002500269952"
    FIRST_NAME = post_code_to_first_name(POST_CODE)
    FIRST_NAME_SELF_CHECK = post_code_to_first_name(POST_CODE_SPECIAL)
    FIRST_NAME_SPECIAL = "azaava"
    LAST_NAME = faker.last_name()

class ApiEntityValues():
    LINK = "http://localhost:8080/api"