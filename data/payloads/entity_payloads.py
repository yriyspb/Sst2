from typing import Dict, Any, Literal
from data.pydantic.models.entities import EntityModel


def get_payload(
        payload_type: Literal["create", "update"] = "create"
) -> Dict[str, Any]:
    templates = {
        "create": {
            "addition": {
                "additional_info": "Дополнительные сведения",
                "additional_number": 747
            },
            "important_numbers": [4, 8, 15, 16, 23, 42],
            "title": "Заголовок сущности",
            "verified": True
        },
        "update": {"addition": {
            "additional_info": "Дополнение дополнительных сведений",
            "additional_number": 787
        },
            "important_numbers": [42],
            "title": "Новый Заголовок сущности",
            "verified": False}
    }

    payload = templates.get(payload_type, templates["create"]).copy()
    return payload


def get_expected_entity(payload_type: str = "create", entity_id: int = None) -> EntityModel:
    payload = get_payload(payload_type)

    if entity_id is not None:
        payload["id"] = entity_id
        payload["addition"]["id"] = entity_id

    return EntityModel(**payload)
