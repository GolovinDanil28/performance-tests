from clients.http.client import HTTPClient
from typing import TypedDict
from httpx import Response


class IssueCardRequestDict(TypedDict):
    """
    Структура данных для создания карты
    """
    userId: str
    accountId: str


class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент взаимодействия с API карт сервиса http-gateway
    """

    def issue_virtual_card_api(self, request: IssueCardRequestDict) -> Response:
        """
        Создание виртуальной карты для указанного пользователя и счета

        :param request: Словарь с данными для создания карты, содержащий:
            userId - идентификатор пользователя
            accountId - идентификатор счета
        :return: Ответ от сервера с деталями созданной карты (объект httpx.Response)
        """
        return self.post("/api/v1/cards/issue-virtual-card", json=request)

    def issue_physical_card_api(self, request: IssueCardRequestDict) -> Response:
        """
        Создание физической карты для указанного пользователя и счета

        :param request: Словарь с данными для создания карты, содержащий:
            userId - идентификатор пользователя
            accountId - идентификатор счета
        :return: Ответ от сервера с деталями созданной карты (объект httpx.Response)
        """
        return self.post("/api/v1/cards/issue-physical-card", json=request)