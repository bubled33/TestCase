import json

from fastapi import APIRouter
from loguru import logger

router = APIRouter(tags=['API Ресурсов'], prefix='/resources_emulation')


@router.get('/json')
async def get_json() -> str:
    """
    Получить данные в формате json.
    Пример: { "data": 300.3, "date":"2023-02-12 00:00"}
    :return: Данные в формате json
    """
    logger.info('json')
    return json.dumps({ "data": 300.3, "date":"2023-02-12 00:00"})


@router.get('/xml')
async def get_xml() -> str:
    """
    Получить данные в формате xml
    Пример: <root><date>12-02-2023 00:00</date><data>200.2</data></root>
    :return: Данные в формате xml
    """
    return '<root><date>12-02-2023 00:00</date><data>200.2</data></root>'


@router.get('/string')
async def get_string() -> str:
    """
    Получить данные в формате строки
    Пример 167612 500.1
    :return: Данные в формате строки
    """
    return "167612 500.1"
