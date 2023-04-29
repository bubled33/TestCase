import asyncio
import json
import re
from contextlib import suppress
from enum import Enum
from json import JSONDecodeError
from re import Pattern
from typing import List

from aiohttp import ClientSession, InvalidURL

from datetime import datetime

from loguru import logger

from config import settings
from database.models import Resource, ResourceResult
from schemas.server_types import ResourceTypes


class ResourceManagerStates(str, Enum):
    working = 'WORKING'
    waiting = 'WAITING'


class ResourceManager:
    """
    """
    def __init__(self, delay: int | None = None):
        """
        :param delay: Задержка между проверками ресурсов. По умолчанию - 1 секунда
        """

        self._delay = delay or 1
        self._client_session: ClientSession | None = None
        self._last_notify_date = datetime.now()
        self._state = ResourceManagerStates.working

    @property
    def state(self) -> ResourceManagerStates:
        return self._state

    @property
    def delay(self) -> int:
        return self._delay

    async def get_result(self, resource: Resource) -> ResourceResult | None:
        """
        Получить данные с ресурса
        :param resource: Ресурс
        :return: Полученные данные
        """
        try:
            response = await self._client_session.get(url=resource.url, data=resource.data or {})
        except InvalidURL:
            return
        # Обработка неверного статуса результата
        if response.status != 200:
            return

        # Получение и валидация данных на основе возвращаемого типа
        if resource.resource_type == ResourceTypes.json:
            try:
                response_args = json.loads(await response.json())
            except JSONDecodeError:
                return
        else:
            response_data = (await response.read()).decode('utf-8')
            response_match = re.match(self._get_pattern(resource.resource_type), response_data)

            # Обработка неправильного формата XML и STRING
            if not response_match:
                return

            response_args = response_match.groupdict()

        # Обработка неправильного формата JSON
        if 'date' not in response_args or 'data' not in response_args:
            return
        date = datetime.strptime(response_args.get('date'), self._get_date_pattern(resource.resource_type))
        data = float(response_args.get('data'))

        return ResourceResult(date=date, data=data)

    async def callback(self):
        """
        Пометить уведомление, как полученное
        :return:
        """
        logger.info('[Менеджер ресурсов] Уведомление получено!')
        self._state = ResourceManagerStates.working

    async def _notify(self):
        """
        Уведомить сервер
        :return:
        """
        if (await ResourceResult.get_data_sum(offset_date=self._last_notify_date) or 0) >= 1000:
            logger.info('[Менеджер ресурсов] Уведомление отправлено!')
            self._last_notify_date = datetime.now()
            await self._client_session.post(settings.Notify.url)
            self._state = ResourceManagerStates.waiting

    async def start(self):
        """
        Запустить менеджер ресурсов
        :return:
        """

        logger.info('[Менеджер ресурсов] Запущен!')
        # Создать новую сессию aiohttp
        self._client_session = ClientSession()
        while True:
            # Если ожидает подтверждение получения уведомления, то не проверяет ресурсы
            if self._state == ResourceManagerStates.waiting:
                await asyncio.sleep(self._delay)
                logger.info('continue')
                continue

            # Проверить ресурсы
            resources = await Resource.all().to_list()
            results: List[ResourceResult | None] = \
                await asyncio.gather(*[self.get_result(resource) for resource in resources])
            with suppress(TypeError):
                await ResourceResult.insert_many([result for result in results if result])

            # Уведомить сервер, если сумма чисел всех полученных данных больше 1000
            await self._notify()
            await asyncio.sleep(self._delay)

    async def stop(self):
        """
        Остановить менеджер ресурсов
        :return:
        """
        await self._client_session.close()

    @classmethod
    def _get_date_pattern(cls, resource_type: ResourceTypes) -> str:
        """
        Получить паттерн для приведения строки в дату определённог формата данных
        :param resource_type:
        :return:
        """
        match resource_type:
            case ResourceTypes.string:
                return '%f'
            case ResourceTypes.xml:
                return '%d-%m-%Y %H:%M'
            case ResourceTypes.json:
                return '%Y-%m-%d %H:%M'
            case _:
                raise ValueError('Неправильный тип формата данных')

    @classmethod
    def _get_pattern(cls, resource_type: ResourceTypes) -> Pattern[str]:
        """
        Получить паттерн для определённого формата данных
        :param resource_type: Формат данных
        :return: Паттерн
        """
        match resource_type:
            case ResourceTypes.string:
                return re.compile(r'"(?P<date>\d+) (?P<data>\d+\.\d+)"')
            case ResourceTypes.xml:
                return re.compile(r'"<root><date>(?P<date>\d{2}-\d{2}-\d{4} \d{2}:\d{2})</date><data>('
                                  r'?P<data>\d+\.\d+)</data></root>"')
            case _:
                raise ValueError('Неправильный тип формата данных')
