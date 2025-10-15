from httpx import Client, URL, QueryParams, Response
from typing import  Any
class HTTPClient:
    """
    Базовый HTTP Api клиент, принимающий объект httpx.Client
    :param client: экземпляр httpx.Client для выполнения HTTP - запросов
    """
    def __init__(self, client: Client):
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) ->  Response:
        """
        Выполняет GET запрос
        :param url: URL адрес эндпоинта
        :param params: GET параметры запроса (напримерб ?key=value)
        :return: Объект Response c данными ответа
        """
        return self.client.get(url, params = params)

    def post(self, url: URL |  str, json: Any | None = None) -> Response:
        """
        Выполняет POST запрос
        :param url: URL адрес эндпоинта
        :param json: Данные в формате JSON
        :return: Объект Response с данными ответа
        """
        return self.client.post(url, json = json)


