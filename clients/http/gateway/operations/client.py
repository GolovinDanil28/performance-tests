from httpx import Response, QueryParams
from locust.env import Environment
from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import build_gateway_http_client, build_gateway_locust_http_client
from clients.http.gateway.operations.schema import (
    GetOperationsQuerySchema,
    GetOperationsSummaryQuerySchema,
    GetOperationResponseSchema,
    GetOperationReceiptResponseSchema,
    GetOperationsResponseSchema,
    GetOperationsSummaryResponseSchema,
    MakeFeeOperationRequestSchema,
    MakeFeeOperationResponseSchema,
    MakeTopUpOperationRequestSchema,
    MakeTopUpOperationResponseSchema,
    MakeCashbackOperationRequestSchema,
    MakeCashbackOperationResponseSchema,
    MakeTransferOperationRequestSchema,
    MakeTransferOperationResponseSchema,
    MakePurchaseOperationRequestSchema,
    MakePurchaseOperationResponseSchema,
    MakeBillPaymentOperationRequestSchema,
    MakeBillPaymentOperationResponseSchema,
    MakeCashWithdrawalOperationRequestSchema,
    MakeCashWithdrawalOperationResponseSchema
)


class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.

    Предоставляет методы для работы с операциями: получение информации об операциях,
    создание различных типов операций, получение статистики и чеков.
    """

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Выполняет GET-запрос для получения информации об операции по её идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Объект httpx.Response с данными об операции.
        """
        return self.get(
            f"/api/v1/operations/{operation_id}",
            extensions=HTTPClientExtensions(route="/api/v1/operations/{operation_id}")
        )

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Выполняет GET-запрос для получения чека операции по её идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Объект httpx.Response с данными чека операции.
        """
        return self.get(
            f"/api/v1/operations/operation-receipt/{operation_id}",
            extensions=HTTPClientExtensions(route="/api/v1/operations/operation-receipt/{operation_id}")
        )

    def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        """
        Выполняет GET-запрос для получения списка операций определенного счета.

        :param query: Pydantic-модель с параметрами запроса.
        :return: Объект httpx.Response со списком операций счета.
        """
        return self.get(
            "/api/v1/operations", 
            params=QueryParams(**query.model_dump(by_alias=True)),
            extensions=HTTPClientExtentions(route="/api/v1/operations")
        )

    def get_operations_summary_api(self, query: GetOperationsSummaryQuerySchema) -> Response:
        """
        Выполняет GET-запрос для получения статистики по операциям определенного счета.

        :param query: Pydantic-модель с параметрами запроса.
        :return: Объект httpx.Response со статистикой операций счета.
        """
        return self.get(
            "/api/v1/operations/operations-summary", 
            params=QueryParams(**query.model_dump(by_alias=True)),
            extensions=HTTPClientExtensions(route="/api/v1/operations/operations-summary")
        )

    def make_fee_operation_api(self, request: MakeFeeOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции комиссии.

        :param request: Pydantic-модель с данными для создания операции комиссии.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request.model_dump(by_alias=True))

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции пополнения.

        :param request: Pydantic-модель с данными для создания операции пополнения.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request.model_dump(by_alias=True))

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции кэшбэка.

        :param request: Pydantic-модель с данными для создания операции кэшбэка.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request.model_dump(by_alias=True))

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции перевода между счетами.

        :param request: Pydantic-модель с данными для создания операции перевода.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request.model_dump(by_alias=True))

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции покупки.

        :param request: Pydantic-модель с данными для создания операции покупки.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request.model_dump(by_alias=True))

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции оплаты по счету.

        :param request: Pydantic-модель с данными для создания операции оплаты по счету.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request.model_dump(by_alias=True))

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestSchema) -> Response:
        """
        Выполняет POST-запрос для создания операции снятия наличных денег.

        :param request: Pydantic-модель с данными для создания операции снятия наличных.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request.model_dump(by_alias=True))

    # High-level methods
    def get_operation(self, operation_id: str) -> GetOperationResponseSchema:
        """
        Получить информацию об операции по её идентификатору (высокоуровневый метод).

        :param operation_id: Идентификатор операции.
        :return: Pydantic-модель с данными операции.
        """
        response = self.get_operation_api(operation_id)
        return GetOperationResponseSchema.model_validate_json(response.text)

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseSchema:
        """
        Получить чек операции по её идентификатору (высокоуровневый метод).

        :param operation_id: Идентификатор операции.
        :return: Pydantic-модель с данными чека операции.
        """
        response = self.get_operation_receipt_api(operation_id)
        return GetOperationReceiptResponseSchema.model_validate_json(response.text)

    def get_operations(self, account_id: str) -> GetOperationsResponseSchema:
        """
        Получить список операций счета (высокоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Pydantic-модель со списком операций.
        """
        query = GetOperationsQuerySchema(account_id=account_id)
        response = self.get_operations_api(query)
        return GetOperationsResponseSchema.model_validate_json(response.text)

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseSchema:
        """
        Получить статистику по операциям счета (высокоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Pydantic-модель со статистикой операций.
        """
        query = GetOperationsSummaryQuerySchema(account_id=account_id)
        response = self.get_operations_summary_api(query)
        return GetOperationsSummaryResponseSchema.model_validate_json(response.text)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseSchema:
        """
        Создать операцию комиссии (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakeFeeOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_fee_operation_api(request)
        return MakeFeeOperationResponseSchema.model_validate_json(response.text)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseSchema:
        """
        Создать операцию пополнения (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakeTopUpOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_top_up_operation_api(request)
        return MakeTopUpOperationResponseSchema.model_validate_json(response.text)

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseSchema:
        """
        Создать операцию кэшбэка (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakeCashbackOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_cashback_operation_api(request)
        return MakeCashbackOperationResponseSchema.model_validate_json(response.text)

    def make_transfer_operation(self, from_account_id: str, to_account_id: str) -> MakeTransferOperationResponseSchema:
        """
        Создать операцию перевода (высокоуровневый метод).

        :param from_account_id: Идентификатор счета отправителя.
        :param to_account_id: Идентификатор счета получателя.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakeTransferOperationRequestSchema(
            from_account_id=from_account_id,
            to_account_id=to_account_id
        )
        response = self.make_transfer_operation_api(request)
        return MakeTransferOperationResponseSchema.model_validate_json(response.text)

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseSchema:
        """
        Создать операцию покупки (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakePurchaseOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_purchase_operation_api(request)
        return MakePurchaseOperationResponseSchema.model_validate_json(response.text)

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseSchema:
        """
        Создать операцию оплаты счета (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakeBillPaymentOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return MakeBillPaymentOperationResponseSchema.model_validate_json(response.text)

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseSchema:
        """
        Создать операцию снятия наличных (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с созданной операцией.
        """
        request = MakeCashWithdrawalOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return MakeCashWithdrawalOperationResponseSchema.model_validate_json(response.text)


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Фабрика для создания клиента OperationsGatewayHTTPClient.

    :return: Экземпляр OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())

def build_operations_gateway_locust_http_client(environment: Environment) -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр OperationsGatewayHTTPClient с хуками сбора метрик.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))