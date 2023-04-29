import asyncio

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app import app
from database.models import Resource, ResourceResult


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope='module')
async def client_test():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://localhost:8080", follow_redirects=True) as client:
            yield client


@pytest_asyncio.fixture(scope='module')
async def clear_database():
    await Resource.delete_all()
    await ResourceResult.delete_all()

    yield

    await Resource.delete_all()
    await ResourceResult.delete_all()
