from typing import TypedDict
from httpx import Response, QueryParams
from clients.http.client import HTTPClient


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