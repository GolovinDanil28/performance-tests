from httpx import Response
from typing import TypedDict
from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class DocumentDict(TypedDict):
    """
    Структура данных для представления документа.

    Attributes:
        url: URL-адрес документа
        document: Содержимое или описание документа
    """
    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос получения документа тарифа.

    Attributes:
        tariff: Объект документа тарифа
    """
    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос получения документа контракта.

    Attributes:
        contract: Объект документа контракта
    """
    contract: DocumentDict


class DocumentsGatewayHTTPClients(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифа по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """

        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self,account_id: str)->Response:
        """
        Получить контракта по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """

        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """
        Получить документ тарифа по счету (высокоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Словарь с данными документа тарифа.
        """
        response = self.get_tariff_document_api(account_id)
        return response.json()

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """
        Получить документ контракта по счету (высокоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Словарь с данными документа контракта.
        """
        response = self.get_contract_document_api(account_id)
        return response.json()

def build_documents_gateway_http_client()->DocumentsGatewayHTTPClients:
    """
    Фабрика для создания клиента DocumentsGatewayHTTPClient.
    :return: Экземпляр DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClients(client=build_gateway_http_client())