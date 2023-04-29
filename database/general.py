from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from database.models import *


async def init_database():
    """
    Инициализирует базу данных
    :return:
    """

    url = 'mongodb://localhost:27017'
    if not settings.Database.is_localhost:
        url = f'mongodb://{settings.Database.user}:{settings.Database.password}' \
              f'@{settings.Database.host}:{settings.Database.port}'
    client = AsyncIOMotorClient(url)

    await init_beanie(database=client[settings.Database.database], document_models=[Resource, ResourceResult])
