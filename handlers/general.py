import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request, HTTPException
from loguru import logger

from database.general import init_database
from untils.resource_manager import ResourceManager, ResourceManagerStates

router = APIRouter(tags=['Основное'], prefix='/general')


@router.get('/ping')
def pong() -> str:
    """
    Проверить работоспособность сервера
    :return:
    """

    return 'pong'


@router.post('/notify')
async def notify():
    """
    Принять уведомление
    :return:
    """
    logger.info('Уведомление получено')


@router.post('/callback')
async def callback(request: Request):
    """
    Оповестить об успешном принятии уведомления
    :param request: Объект запроса
    :return:
    """
    resource_manager: ResourceManager = request.app.state.resource_manager
    if resource_manager.state != ResourceManagerStates.waiting:
        return HTTPException(status_code=1, detail='123')
    logger.info('Отправлено подтверждение для уведомления')
    await resource_manager.callback()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Жизненный цикл сервера
    :param app: Объект сервера
    :return:
    """
    resource_manager = ResourceManager()
    app.state.resource_manager = resource_manager
    await init_database()
    asyncio.create_task(resource_manager.start())
    yield
    await resource_manager.stop()
