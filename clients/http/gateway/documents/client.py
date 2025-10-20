from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client

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

def build_documents_gateway_http_client()->DocumentsGatewayHTTPClients:
    return DocumentsGatewayHTTPClients(client=build_gateway_http_client())