import allure

from helpers.api_client import ApiClient

from data.payloads.entity_payloads import (
    get_payload,
    get_expected_entity
)


class TestEntityAPI:

    def setup_method(self):
        self.client = ApiClient()

    @allure.title("Позитивный тест создания сущности(POST)")
    def test_create_entity_positive(self):
        response = self.client.create_entity()

        with allure.step('Проверяем тело ответа'):
            assert response, "ID сущности не должен быть пустым"

    @allure.title("Позитивный тест получения сущности(GET)")
    def test_get_entity_positive(self, create_entity):
        entity_id = create_entity

        expected_model = get_expected_entity("create", entity_id)

        with allure.step('Делаем GET запрос для получения сущности'):
            actual_model = self.client.get_entity(entity_id)

        with allure.step('Проверяем тело ответа'):
            expected_dict = expected_model.dict()
            actual_dict = actual_model.dict()
            assert expected_dict == actual_dict, f"Данные не совпадают:\nОжидалось: {expected_dict}\nПолучено: {actual_dict}"

    @allure.title("Позитивный тест получения всех сущностей(GET)")
    def test_get_all_entities_positive(self, create_entity):
        with allure.step('Делаем GET запрос для получения всех сущностей'):
            response = self.client.get_all_entities()

        with allure.step('Проверяем тело ответа'):
            assert isinstance(response.entity, list)

    @allure.title("Позитивный тест обновления сущности(PATCH)")
    def test_patch_entity_positive(self, create_entity):
        entity_id = create_entity

        patch_payload = get_payload("update")
        expected_model = get_expected_entity("update", entity_id)

        with allure.step('Делаем PATCH запрос с телом для обновления сущности'):
            self.client.update_entity(entity_id, patch_payload)

        with allure.step('Делаем GET запрос для проверки обновления сущности'):
            actual_model = self.client.get_entity(entity_id)

        with allure.step('Проверяем тело ответа'):
            expected_dict = expected_model.dict()
            actual_dict = actual_model.dict()
            assert expected_dict == actual_dict, f"Данные не совпадают:\nОжидалось: {expected_dict}\nПолучено: {actual_dict}"

    @allure.title("Позитивный тест удаления сущности(DELETE)")
    def test_delete_entity_positive(self, create_entity):
        entity_id = create_entity

        with allure.step('Делаем DELETE запрос для удаления сущности'):
            response = self.client.delete_entity(entity_id)

        with allure.step('Делаем GET запрос с id удаленной сущности'):
            deleted_response = self.client.get_no_entity(entity_id)
