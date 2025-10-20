from typing import TypedDict
from httpx import Response, QueryParams
from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class OperationDict(TypedDict):
    """
    Структура данных для представления операции.

    Attributes:
        id: Идентификатор операции
        type: Тип операции (FEE, TOP_UP, CASHBACK и т.д.)
        status: Статус операции (FAILED, COMPLETED и т.д.)
        amount: Сумма операции
        cardId: Идентификатор карты
        category: Категория операции
        createdAt: Время создания операции
        accountId: Идентификатор счета
    """
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """
    Структура данных для представления чека операции.

    Attributes:
        url: URL-адрес чека
        document: Содержимое или описание чека
    """
    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    """
    Структура данных для представления сводки по операциям.

    Attributes:
        spentAmount: Потраченная сумма
        receivedAmount: Полученная сумма
        cashbackAmount: Сумма кэшбэка
    """
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


# Response TypedDict classes
class GetOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос получения операции.

    Attributes:
        operation: Объект операции
    """
    operation: OperationDict


class GetOperationReceiptResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос получения чека операции.

    Attributes:
        receipt: Объект чека операции
    """
    receipt: OperationReceiptDict


class GetOperationsResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос получения списка операций.

    Attributes:
        operations: Список операций
    """
    operations: list[OperationDict]


class GetOperationsSummaryResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос получения сводки по операциям.

    Attributes:
        summary: Сводка по операциям
    """
    summary: OperationsSummaryDict


class MakeFeeOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции комиссии.

    Attributes:
        operation: Созданная операция комиссии
    """
    operation: OperationDict


class MakeTopUpOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции пополнения.

    Attributes:
        operation: Созданная операция пополнения
    """
    operation: OperationDict


class MakeCashbackOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции кэшбэка.

    Attributes:
        operation: Созданная операция кэшбэка
    """
    operation: OperationDict


class MakeTransferOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции перевода.

    Attributes:
        operation: Созданная операция перевода
    """
    operation: OperationDict


class MakePurchaseOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции покупки.

    Attributes:
        operation: Созданная операция покупки
    """
    operation: OperationDict


class MakeBillPaymentOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции оплаты счета.

    Attributes:
        operation: Созданная операция оплаты счета
    """
    operation: OperationDict


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    """
    Структура данных для ответа на запрос создания операции снятия наличных.

    Attributes:
        operation: Созданная операция снятия наличных
    """
    operation: OperationDict


# Query and Request TypedDict classes
class GetOperationQueryDict(TypedDict):
    """
    Структура данных для получения информации об операции.
    """
    operation_id: str


class GetOperationReceiptQueryDict(TypedDict):
    """
    Структура данных для получения чека операции.
    """
    operation_id: str


class GetOperationsQueryDict(TypedDict):
    """
    Структура данных для получения списка операций счета.
    """
    accountId: str


class GetOperationsSummaryQueryDict(TypedDict):
    """
    Структура данных для получения статистики по операциям.
    """
    accountId: str


class BaseOperationRequestDict(TypedDict):
    """
    Базовая структура данных для создания операций.
    """
    status: str
    amount: float


class CardOperationRequestDict(BaseOperationRequestDict):
    """
    Базовая структура данных для операций с картой.
    """
    cardId: str
    accountId: str


class MakeFeeOperationRequestDict(CardOperationRequestDict):
    """
    Структура данных для создания операции комиссии.
    """
    pass


class MakeTopUpOperationRequestDict(CardOperationRequestDict):
    """
    Структура данных для создания операции пополнения.
    """
    pass


class MakeCashbackOperationRequestDict(CardOperationRequestDict):
    """
    Структура данных для создания операции кэшбэка.
    """
    pass


class MakeTransferOperationRequestDict(BaseOperationRequestDict):
    """
    Структура данных для создания операции перевода.
    """
    fromAccountId: str
    toAccountId: str


class MakePurchaseOperationRequestDict(CardOperationRequestDict):
    """
    Структура данных для создания операции покупки.
    """
    category: str
    merchant: str


class MakeBillPaymentOperationRequestDict(CardOperationRequestDict):
    """
    Структура данных для создания операции оплаты по счету.
    """
    billId: str
    paymentPurpose: str


class MakeCashWithdrawalOperationRequestDict(CardOperationRequestDict):
    """
    Структура данных для создания операции снятия наличных.
    """
    atmId: str


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
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Выполняет GET-запрос для получения чека операции по её идентификатору.

        :param operation_id: Идентификатор операции.
        :return: Объект httpx.Response с данными чека операции.
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Выполняет GET-запрос для получения списка операций определенного счета.

        :param query: Словарь с параметрами запроса, должен содержать accountId.
        :return: Объект httpx.Response со списком операций счета.
        """
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Выполняет GET-запрос для получения статистики по операциям определенного счета.

        :param query: Словарь с параметрами запроса, должен содержать accountId.
        :return: Объект httpx.Response со статистикой операций счета.
        """
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции комиссии.

        :param request: Словарь с данными для создания операции комиссии. Должен содержать status, amount, accountId, cardId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции пополнения.

        :param request: Словарь с данными для создания операции пополнения. Должен содержать status, amount, accountId, cardId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции кэшбэка.

        :param request: Словарь с данными для создания операции кэшбэка. Должен содержать status, amount, accountId, cardId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции перевода между счетами.

        :param request: Словарь с данными для создания операции перевода. Должен содержать status, amount, fromAccountId, toAccountId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции покупки.

        :param request: Словарь с данными для создания операции покупки. Должен содержать status, amount, accountId, cardId, category, merchant.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции оплаты по счету.

        :param request: Словарь с данными для создания операции оплаты по счету. Должен содержать status, amount, accountId, cardId, billId, paymentPurpose.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос для создания операции снятия наличных денег.

        :param request: Словарь с данными для создания операции снятия наличных. Должен содержать status, amount, accountId, cardId, atmId.
        :return: Объект httpx.Response с результатом создания операции.
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)

    # High-level methods
    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """
        Получить информацию об операции по её идентификатору (высокоуровневый метод).

        :param operation_id: Идентификатор операции.
        :return: Словарь с данными операции.
        """
        response = self.get_operation_api(operation_id)
        return response.json()

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """
        Получить чек операции по её идентификатору (высокоуровневый метод).

        :param operation_id: Идентификатор операции.
        :return: Словарь с данными чека операции.
        """
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """
        Получить список операций счета (высокоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Словарь со списком операций.
        """
        query = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """
        Получить статистику по операциям счета (высокоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Словарь со статистикой операций.
        """
        query = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(query)
        return response.json()

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        """
        Создать операцию комиссии (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с созданной операцией.
        """
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseDict:
        """
        Создать операцию пополнения (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с созданной операцией.
        """
        request = MakeTopUpOperationRequestDict(
            status="COMPLETED",
            amount=1500.11,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseDict:
        """
        Создать операцию кэшбэка (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с созданной операцией.
        """
        request = MakeCashbackOperationRequestDict(
            status="COMPLETED",
            amount=25.50,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation(self, from_account_id: str, to_account_id: str) -> MakeTransferOperationResponseDict:
        """
        Создать операцию перевода (высокоуровневый метод).

        :param from_account_id: Идентификатор счета отправителя.
        :param to_account_id: Идентификатор счета получателя.
        :return: Словарь с созданной операцией.
        """
        request = MakeTransferOperationRequestDict(
            status="COMPLETED",
            amount=1000.0,
            fromAccountId=from_account_id,
            toAccountId=to_account_id
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseDict:
        """
        Создать операцию покупки (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с созданной операцией.
        """
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=500.75,
            cardId=card_id,
            accountId=account_id,
            category="shopping",
            merchant="Online Store"
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseDict:
        """
        Создать операцию оплаты счета (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с созданной операцией.
        """
        request = MakeBillPaymentOperationRequestDict(
            status="COMPLETED",
            amount=250.0,
            cardId=card_id,
            accountId=account_id,
            billId="bill_12345",
            paymentPurpose="Utility payment"
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation(self, card_id: str, account_id: str) -> MakeCashWithdrawalOperationResponseDict:
        """
        Создать операцию снятия наличных (высокоуровневый метод).

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с созданной операцией.
        """
        request = MakeCashWithdrawalOperationRequestDict(
            status="COMPLETED",
            amount=300.0,
            cardId=card_id,
            accountId=account_id,
            atmId="atm_67890"
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Фабрика для создания клиента OperationsGatewayHTTPClient.

    :return: Экземпляр OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())