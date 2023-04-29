from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter

from database.models import Resource
from schemas.resource import ResourceIn, ResourceOut

router = APIRouter(tags=['API Ресурсов'], prefix='/resources')


@router.post('/create')
async def create_router(instance_date: ResourceIn) -> ResourceOut:
    """
    Добавить новый ресурс
    :param instance_date: Информауия о ресурсе
    :return: Объект ресурса
    """
    return (await Resource(**instance_date.dict()).create()).out


@router.post('/get')
async def get_router(instance_id: PydanticObjectId) -> ResourceOut | None:
    """
    Получить ресурс по ID
    :param instance_id: ID ресурса
    :return: Объект ресурса
    """
    instance = await Resource.get(instance_id)
    if not instance:
        return None
    return instance.out


@router.post('/get_all')
async def get_all() -> List[ResourceOut]:
    """
    Получить список всех ресурсов
    :return: Список ресурсов
    """
    return [resource.out for resource in await Resource.all().to_list()]


@router.post('/delete')
async def delete_router(instance_id: PydanticObjectId):
    """
    Удалить ресурс по ID
    :param instance_id: ID ресурса
    :return:
    """
    await Resource.find_one(Resource.id == instance_id).delete_one()
