from helpers import generate_post_code, post_code_to_first_name
from faker import Faker

faker = Faker()


class ManagerPageValues():

    LINK = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager"
    POST_CODE_SPECIAL = "002500269952"
    FIRST_NAME_SELF_CHECK = post_code_to_first_name(POST_CODE_SPECIAL)
    FIRST_NAME_SPECIAL = "azaava"

    @staticmethod
    def post_code():
        return generate_post_code()

    @staticmethod
    def first_name():
        return post_code_to_first_name(ManagerPageValues.post_code())

    @staticmethod
    def last_name():
        return faker.last_name()
