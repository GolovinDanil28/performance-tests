from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from uuid import UUID, uuid4


class UserSchema(BaseModel):
    """
    Модель данных пользователя.

    Используется для представления полной информации о пользователе
    во всех ответах API.

    Attributes:
        id: UUID пользователя
        email: Email пользователя
        lastName: Фамилия пользователя
        firstName: Имя пользователя
        middleName: Отчество пользователя (опционально)
        phoneNumber: Номер телефона пользователя
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "lastName": "Иванов",
                "firstName": "Иван",
                "middleName": "Иванович",
                "phoneNumber": "+79991234567"
            }
        }
    )

    id: UUID = Field(
        default_factory=uuid4,
        description="Уникальный идентификатор пользователя"
    )
    email: EmailStr = Field(
        description="Email адрес пользователя"
    )
    lastName: str = Field(
        min_length=1,
        max_length=100,
        description="Фамилия пользователя"
    )
    firstName: str = Field(
        min_length=1,
        max_length=100,
        description="Имя пользователя"
    )
    middleName: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Отчество пользователя"
    )
    phoneNumber: str = Field(
        min_length=5,
        max_length=20,
        description="Номер телефона пользователя"
    )


class CreateUserRequestSchema(BaseModel):
    """
    Модель запроса на создание пользователя.

    Используется для валидации входящих данных при создании пользователя.
    Не включает поле id, так как оно генерируется автоматически.

    Attributes:
        email: Email пользователя
        lastName: Фамилия пользователя
        firstName: Имя пользователя
        middleName: Отчество пользователя (опционально)
        phoneNumber: Номер телефона пользователя
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "lastName": "Иванов",
                "firstName": "Иван",
                "middleName": "Иванович",
                "phoneNumber": "+79991234567"
            }
        }
    )

    email: EmailStr = Field(
        description="Email адрес пользователя"
    )
    lastName: str = Field(
        min_length=1,
        max_length=100,
        description="Фамилия пользователя"
    )
    firstName: str = Field(
        min_length=1,
        max_length=100,
        description="Имя пользователя"
    )
    middleName: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Отчество пользователя"
    )
    phoneNumber: str = Field(
        min_length=5,
        max_length=20,
        description="Номер телефона пользователя"
    )


class CreateUserResponseSchema(BaseModel):
    """
    Модель ответа с данными созданного пользователя.

    Используется для возврата данных после успешного создания пользователя.
    Содержит объект пользователя в поле user.

    Attributes:
        user: Объект с данными созданного пользователя
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "lastName": "Иванов",
                    "firstName": "Иван",
                    "middleName": "Иванович",
                    "phoneNumber": "+79991234567"
                }
            }
        }
    )

    user: UserSchema = Field(
        description="Данные созданного пользователя"
    )