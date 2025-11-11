from typing import Dict, Any


def get_default_create_payload() -> Dict[str, Any]:
    return {
        "addition": {
            "additional_info": "Дополнительные сведения",
            "additional_number": 747
        },
        "important_numbers": [4, 8, 15, 16, 23, 42],
        "title": "Заголовок сущности",
        "verified": True
    }


def get_full_update_payload() -> Dict[str, Any]:
    return {
        "addition": {
            "additional_info": "Дополнение дополнительных сведений",
            "additional_number": 787
        },
        "important_numbers": [42],
        "title": "Новый Заголовок сущности",
        "verified": False
    }
