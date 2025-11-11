# tests/api_client.py
import os
import requests
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from data.pydantic.models.entities import (
    CreateResponseModel,
    GetResponseModel,
    GetAllResponseModel,
    UpdateResponseModel,
    DeleteResponseModel
)
from data.payloads.entity_payloads import get_payload

load_dotenv()


class ApiClient:

    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.timeout = int(os.getenv('TEST_TIMEOUT', '5'))

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def create_entity(self, payload: Optional[Dict[str, Any]] = None) -> CreateResponseModel:
        payload = get_payload("create")

        response = requests.post(
            url=f"{self.base_url}/create",
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(f"Ошибка создания сущности. Status: {response.status_code}, Response: {response.text}")

        response_data = response.json()
        return response_data

    def get_entity(self, entity_id: int) -> GetResponseModel:
        response = requests.get(
            url=f"{self.base_url}/get/{entity_id}",
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(
                f"Ошибка получения сущности {entity_id}. Status: {response.status_code}, Response: {response.text}")

        response_data = response.json()
        return GetResponseModel(**response_data)

    def get_no_entity(self, entity_id: int) -> GetResponseModel:
        response = requests.get(
            url=f"{self.base_url}/get/{entity_id}",
            timeout=self.timeout
        )

        if response.status_code != 500:
            raise Exception(
                f"Сущность {entity_id} не удалена. Status: {response.status_code}, Response: {response.text}")

    def get_all_entities(self) -> GetAllResponseModel:
        response = requests.get(
            url=f"{self.base_url}/getAll",
            timeout=self.timeout
        )

        if response.status_code != 200:
            raise Exception(
                f"Ошибка получения списка сущностей. Status: {response.status_code}, Response: {response.text}")

        response_data = response.json()

        for entity in GetAllResponseModel(**response_data).entity:
            GetResponseModel(**entity.dict())

        return GetAllResponseModel(**response_data)

    def update_entity(self, entity_id: int, patch_payload: Dict[str, Any]) -> UpdateResponseModel:
        response = requests.patch(
            url=f"{self.base_url}/patch/{entity_id}",
            json=patch_payload,
            headers=self.headers,
            timeout=self.timeout
        )

        if response.status_code != 204:
            raise Exception(
                f"Ошибка обновления сущности {entity_id}. Status: {response.status_code}, Response: {response.text}")

    def delete_entity(self, entity_id: int) -> DeleteResponseModel:
        response = requests.delete(
            url=f"{self.base_url}/delete/{entity_id}",
            timeout=self.timeout
        )

        if response.status_code != 204:
            raise Exception(
                f"Ошибка удаления сущности {entity_id}. Status: {response.status_code}, Response: {response.text}")

    def create_test_entity(self) -> int:
        response = self.create_entity()
        entity_id = response
        return entity_id

    def cleanup_entity(self, entity_id: int):
        if not entity_id:
            return
        try:
            self.delete_entity(entity_id)
        except Exception as e:
            print(f"⚠️  Ошибка при удалении сущности {entity_id}: {e}")
