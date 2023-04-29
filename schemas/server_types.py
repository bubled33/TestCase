from __future__ import annotations

from enum import Enum


class ResourceTypes(str, Enum):
    """
    Типы возвращаемых данных ресурсом

    :param :xml Данные в формате XML. Пример: <root><date>12-02-2023 00:00</date><data>200.2</data></root>
    :param :json Данные в формате JSON. Пример: { "data": 300.3, "date":"2023-02-12 00:00"}
    :param :string Данные в формате STRING. Пример: "167612 500.1"
    """
    xml = 'XML'
    json = 'JSON'
    string = 'STRING'
