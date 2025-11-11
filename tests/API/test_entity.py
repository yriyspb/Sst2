import requests
import allure

from data.pydantic.models.entities import (
    GetResponseModel,
    GetAllResponseModel,
)
from data.payloads.entity_payloads import (
    get_default_create_payload,
    get_full_update_payload
)

from data.values import ApiEntityValues


class TestEntityAPI:
    BASE_URL = ApiEntityValues.LINK

    @allure.title("Позитивный тест создания сущности(POST)")
    def test_create_entity_positive(self):
        payload = get_default_create_payload()

        with allure.step('Делаем POST запрос с телом для создания сущности'):
            response = requests.post(
                url=f"{self.BASE_URL}/create",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

        with allure.step('Сравниваем код ответа'):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        response_data = response.json()
        deserialized_response_id = response_data

        with allure.step('Проверяем тело ответа'):
            assert deserialized_response_id, "ID сущности не должен быть пустым"

        return deserialized_response_id

    @allure.title("Позитивный тест получения сущности(GET)")
    def test_get_entity_positive(self):
        entity_id = self.test_create_entity_positive()

        post_payload = get_default_create_payload()
        addition_payload = post_payload['addition']

        with allure.step('Делаем GET запрос для получения сущности'):
            response = requests.get(
                url=f"{self.BASE_URL}/get/{entity_id}",
                timeout=5
            )

        with allure.step('Сравниваем код ответа'):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        response_data = response.json()

        deserialized_response = GetResponseModel(**response_data)

        with allure.step('Проверяем тело ответа'):
            assert deserialized_response.id == entity_id, "Поле id не соответствует"
            assert deserialized_response.title == post_payload['title'], "Поле title не соответствует"
            assert deserialized_response.verified == post_payload['verified'], "Поле verified не соответствует"
            assert deserialized_response.important_numbers == post_payload[
                'important_numbers'], "Поле important_numbers не соответствует"
            assert deserialized_response.addition.additional_info == addition_payload[
                'additional_info'], "Поле additional_info не соответствует"
            assert deserialized_response.addition.additional_number == addition_payload[
                'additional_number'], "Поле additional_number не соответствует"
            assert deserialized_response.addition.id == entity_id, "Поле addition id не соответствует"

        self._cleanup_entity(entity_id)

        return deserialized_response

    @allure.title("Позитивный тест получения всех сущностей(GET)")
    def test_get_all_entities_positive(self):

        with allure.step('Делаем GET запрос для получения всех сущностей'):
            response = requests.get(
                url=f"{self.BASE_URL}/getAll",
                timeout=5
            )

        with allure.step('Сравниваем код ответа'):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        response_data = response.json()

        deserialized_response = GetAllResponseModel(**response_data)

        with allure.step('Проверяем тело ответа'):
            assert isinstance(deserialized_response.entity, list)

        for entity in deserialized_response.entity:
            GetResponseModel(**entity.dict())

        return deserialized_response

    @allure.title("Позитивный тест обновления сущности(PATCH)")
    def test_patch_entity_positive(self):
        entity_id = self.test_create_entity_positive()

        patch_payload = get_full_update_payload()
        addition_payload = patch_payload['addition']

        with allure.step('Делаем PATCH запрос с телом для обновления сущности'):
            response = requests.patch(
                url=f"{self.BASE_URL}/patch/{entity_id}",
                json=patch_payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

        with allure.step('Сравниваем код ответа'):
            assert response.status_code == 204, f"Ожидался статус 204, получен {response.status_code}"

        with allure.step('Делаем GET запрос для проверки обновления сущности'):
            updated_response = requests.get(
                url=f"{self.BASE_URL}/get/{entity_id}",
                timeout=5
            )

        response_data = updated_response.json()

        with allure.step('Сравниваем код ответа'):
            assert updated_response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        updated_data = GetResponseModel(**response_data)

        with allure.step('Проверяем тело ответа'):
            assert updated_data.id == entity_id, "Поле id не соответствует"
            assert updated_data.title == patch_payload['title'], "Поле title не соответствует"
            assert updated_data.verified is patch_payload['verified'], "Поле verified не соответствует"
            assert updated_data.important_numbers == patch_payload[
                'important_numbers'], "Поле important_numbers не соответствует"
            assert updated_data.addition.additional_info == addition_payload[
                'additional_info'], "Поле additional_info не соответствует"
            assert updated_data.addition.additional_number == addition_payload[
                'additional_number'], "Поле additional_number не соответствует"
            assert updated_data.addition.id == entity_id, "Поле addition id не соответствует"

        self._cleanup_entity(entity_id)

        return updated_data

    @allure.title("Позитивный тест удаления сущности(DELETE)")
    def test_delete_entity_positive(self):
        entity_id = self.test_create_entity_positive()

        with allure.step('Делаем DELETE запрос для удаления сущности'):
            response = requests.delete(
                url=f"{self.BASE_URL}/delete/{entity_id}",
                timeout=5
            )

        with allure.step('Сравниваем код ответа'):
            assert response.status_code == 204, f"Ожидался статус 204, получен {response.status_code}"

        with allure.step('Делаем GET запрос с id удаленной сущности'):
            deleted_response = requests.get(
                url=f"{self.BASE_URL}/get/{entity_id}",
                timeout=5
            )

        with allure.step('Сравниваем код ответа'):
            assert deleted_response.status_code == 500, "Сущность не удалена!"

    def _cleanup_entity(self, entity_id: str):
        try:
            requests.delete(f"{self.BASE_URL}/delete/{entity_id}")
        except:
            pass
