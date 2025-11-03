from pydantic import BaseModel, Field, ConfigDict


class DocumentSchema(BaseModel):
    """
    Структура данных для представления документа.

    Attributes:
        url: URL-адрес документа
        document: Содержимое или описание документа
    """
    model_config = ConfigDict(populate_by_name=True)

    url: str
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос получения документа тарифа.

    Attributes:
        tariff: Объект документа тарифа
    """
    model_config = ConfigDict(populate_by_name=True)

    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    Структура данных для ответа на запрос получения документа контракта.

    Attributes:
        contract: Объект документа контракта
    """
    model_config = ConfigDict(populate_by_name=True)

    contract: DocumentSchema