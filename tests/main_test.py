import pytest
from httpx import AsyncClient

from database.models import Resource


@pytest.mark.asyncio
async def test_ping(client_test: AsyncClient):
    response = await client_test.get('/api/general/ping')
    assert response.status_code == 200
    assert (response.read()).decode('utf-8') == '"pong"'


@pytest.mark.asyncio
async def test_create_resource(client_test: AsyncClient):
    response = await client_test.post('/api/resources/create', json={'url': 'test_url', 'resource_type': 'JSON'})
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
async def test_get_resource(client_test: AsyncClient):
    resource = await Resource(url='test_url', resource_type='JSON').create()
    response = await client_test.post(f'/api/resources/get?instance_id={resource.id}')
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
async def test_get_all_resources(client_test: AsyncClient):
    response = await client_test.post(f'/api/resources/get_all')
    assert response.status_code == 200
    assert response.json()


@pytest.mark.asyncio
async def test_delete_resource(client_test: AsyncClient):
    resource = await Resource(url='test_url', resource_type='JSON').create()
    response = await client_test.post(f'/api/resources/delete?instance_id={resource.id}')
    assert response.status_code == 200
