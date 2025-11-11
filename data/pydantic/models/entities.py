from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class AdditionModel(BaseModel):
    id: Optional[int] = None
    additional_info: str
    additional_number: int


class EntityModel(BaseModel):
    id: int
    addition: AdditionModel
    important_numbers: List[int]
    title: str
    verified: bool


class GetResponseModel(BaseModel):
    id: int
    addition: AdditionModel
    important_numbers: List[int]
    title: str
    verified: bool


class GetRequestModel(BaseModel):
    id: int
    addition: AdditionModel
    important_numbers: List[int]
    title: str
    verified: bool


class GetAllResponseModel(BaseModel):
    entity: List[GetResponseModel]


class CreateResponseModel(BaseModel):
    id: int
    status: str
    created_entity: EntityModel


class UpdateResponseModel(BaseModel):
    id: int
    status: str
    updated_entity: EntityModel
    updated_fields: List[str]


class DeleteResponseModel(BaseModel):
    id: int
    status: str
    message: Optional[str] = None


class PatchRequestModel(BaseModel):
    title: Optional[str] = None
    verified: Optional[bool] = None
    important_numbers: Optional[List[int]] = None
    addition: Optional[Dict[str, Any]] = None
