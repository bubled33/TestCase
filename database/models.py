from datetime import datetime
from typing import Dict, Any

from beanie import Document
from pydantic import Field

from schemas.resource import ResourceOut, ResourceIn
from schemas.server_types import ResourceTypes


class Resource(Document):
    """
    Ресурс

    :param url: API URL Ресурса
    :param data: Данные, которые необходимо передавать в GET запросе. Опционально
    :param resource_type: Тип возвращаемых данных
    """
    url: str
    data: Dict[str, Any] | None = None
    resource_type: ResourceTypes

    @classmethod
    def from_in(cls, instance_data: ResourceIn):
        """
        Преобразовать входные данные в объект БД
        :param instance_data: Входные данные
        :return: Объект БД
        """
        return Resource(url=instance_data.url,
                        data=instance_data.data,
                        resource_type=instance_data.resource_type)

    @property
    def out(self) -> ResourceOut:
        """
        Преобразовать текущий объект БД в выходные данные
        :return: Выходные данные
        """
        return ResourceOut(url=self.url,
                           data=self.data,
                           resource_type=self.resource_type,
                           id=self.id)


class ResourceResult(Document):
    """
    Результат ресурса

    :param :created_date Дата получения
    :param :data Число
    :param "date Дата

    """
    created_date: datetime = Field(default_factory=datetime.now)
    data: float
    date: datetime

    @classmethod
    async def get_data_sum(cls, offset_date: datetime | None = None) -> float:
        """
        Получить сумму всех результатов, начиная с offset_date, если не указан, то берутся все результаты
        :param offset_date: Начиная с какой даты брать
        :return: Сумма полей data
        """
        if not offset_date:
            instances = ResourceResult.find_all()
        else:
            instances = ResourceResult.find_all(ResourceResult.created_date >= offset_date)
        return await instances.sum('data')


__all__ = ['ResourceResult', 'Resource']
