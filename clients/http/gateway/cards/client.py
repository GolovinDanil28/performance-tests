from clients.http.client import HTTPClient
from typing import TypedDict
from httpx import Response, request
from clients.http.gateway.client import build_gateway_http_client


class CardDict(TypedDict):
    id:str
    pin:str
    cvv:str
    type:str
    status: str
    accountId: str
    cardNumber: str
    cardHolder: str
    expiryDate: str
    paymentSystem: str



class IssueCardRequestDict(TypedDict):
    """
    Структура данных для создания карты
    """
    userId: str
    accountId: str

class IssueCardResponseDict(TypedDict):
    card: CardDict


class IssuePhysicalCardRequestDict(TypedDict):
    """
    Структура данных для создания карты
    """
    userId: str
    accountId: str

class IssueVirtualCardRequestDict(TypedDict):
    """
    Структура данных для создания карты
    """
    userId: str
    accountId: str

class IssueVirtualCardResponseDict(TypedDict):
    card: CardDict

class IssuePhysicalCardResponseDict(TypedDict):
    card: CardDict


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

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseDict:
        request = IssueCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_virtual_card_api(request)
        return response.json()

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseDict:
        request = IssueCardRequestDict(userId=user_id, accountId=account_id)
        response = self.issue_physical_card_api(request)
        return response.json()

def build_cards_gateway_http_client()->CardsGatewayHTTPClient:
    return CardsGatewayHTTPClient(client=build_gateway_http_client())