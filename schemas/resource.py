from typing import Dict, Any

from beanie import PydanticObjectId
from pydantic import BaseModel

from schemas.server_types import ResourceTypes


class ResourceIn(BaseModel):
    """
    Входные данные ресурса

    :param url: API URL Ресурса
    :param data: Данные, которые необходимо передавать в GET запросе. Опционально
    :param resource_type: Тип возвращаемых данных
    """

    url: str
    data: Dict[str, Any] | None = None
    resource_type: ResourceTypes


class ResourceOut(BaseModel):
    """
    Выходные данные ресурса

    :param url: API URL Ресурса
    :param data: Данные, которые необходимо передавать в GET запросе. Опционально
    :param resource_type: Тип возвращаемых данных
    :param id: ID ресурса
    """

    url: str
    data: Dict[str, Any] | None = None
    resource_type: ResourceTypes
    id: PydanticObjectId
