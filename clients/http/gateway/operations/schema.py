from enum import StrEnum
from pydantic import BaseModel, Field, ConfigDict


class OperationType(StrEnum):
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    PURCHASE = "PURCHASE"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class OperationStatus(StrEnum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"


class OperationSchema(BaseModel):
    """
    Структура данных для представления операции.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str
    created_at: str = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """
    Структура данных для представления чека операции.
    """
    model_config = ConfigDict(populate_by_name=True)

    url: str
    document: str


class OperationsSummarySchema(BaseModel):
    """
    Структура данных для представления сводки по операциям.
    """
    model_config = ConfigDict(populate_by_name=True)

    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


# Response Schemas
class GetOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос получения операции.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class GetOperationReceiptResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос получения чека операции.
    """
    model_config = ConfigDict(populate_by_name=True)

    receipt: OperationReceiptSchema


class GetOperationsResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос получения списка операций.
    """
    model_config = ConfigDict(populate_by_name=True)

    operations: list[OperationSchema]


class GetOperationsSummaryResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос получения сводки по операциям.
    """
    model_config = ConfigDict(populate_by_name=True)

    summary: OperationsSummarySchema


class MakeFeeOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции комиссии.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class MakeTopUpOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции пополнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class MakeCashbackOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции кэшбэка.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class MakeTransferOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции перевода.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class MakePurchaseOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции покупки.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции оплаты счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос создания операции снятия наличных.
    """
    model_config = ConfigDict(populate_by_name=True)

    operation: OperationSchema


# Query and Request Schemas
class GetOperationsQuerySchema(BaseModel):
    """
    Структура данных для получения списка операций счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsSummaryQuerySchema(BaseModel):
    """
    Структура данных для получения статистики по операциям.
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class BaseOperationRequestSchema(BaseModel):
    """
    Базовая структура данных для создания операций.
    """
    model_config = ConfigDict(populate_by_name=True)

    status: OperationStatus
    amount: float


class CardOperationRequestSchema(BaseOperationRequestSchema):
    """
    Базовая структура данных для операций с картой.
    """
    model_config = ConfigDict(populate_by_name=True)

    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeFeeOperationRequestSchema(CardOperationRequestSchema):
    """
    Структура данных для создания операции комиссии.
    """
    pass


class MakeTopUpOperationRequestSchema(CardOperationRequestSchema):
    """
    Структура данных для создания операции пополнения.
    """
    pass


class MakeCashbackOperationRequestSchema(CardOperationRequestSchema):
    """
    Структура данных для создания операции кэшбэка.
    """
    pass


class MakeTransferOperationRequestSchema(BaseOperationRequestSchema):
    """
    Структура данных для создания операции перевода.
    """
    model_config = ConfigDict(populate_by_name=True)

    from_account_id: str = Field(alias="fromAccountId")
    to_account_id: str = Field(alias="toAccountId")


class MakePurchaseOperationRequestSchema(CardOperationRequestSchema):
    """
    Структура данных для создания операции покупки.
    """
    model_config = ConfigDict(populate_by_name=True)

    category: str
    merchant: str


class MakeBillPaymentOperationRequestSchema(CardOperationRequestSchema):
    """
    Структура данных для создания операции оплаты по счету.
    """
    model_config = ConfigDict(populate_by_name=True)

    bill_id: str = Field(alias="billId")
    payment_purpose: str = Field(alias="paymentPurpose")


class MakeCashWithdrawalOperationRequestSchema(CardOperationRequestSchema):
    """
    Структура данных для создания операции снятия наличных.
    """
    model_config = ConfigDict(populate_by_name=True)

    atm_id: str = Field(alias="atmId")