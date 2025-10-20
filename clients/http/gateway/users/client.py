from clients.http.client import HTTPClient
from typing import TypedDict
from httpx import Response, Client
from clients.http.gateway.client import build_gateway_http_client

from faker import Faker

fake = Faker()

class UserDict(TypedDict):
    id: str
    email: str
    lastName: str
    firstName:str
    middleName: str
    phoneNumber: str

class GetUserResponseDict(TypedDict):
    user: UserDict

class CreateUserRequestDict(TypedDict):
    """
    Структура данных для создания нового пользователя
    """
    email: str
    lastName: str
    firstName: str
    middleName: str
    phoneNumber: str



class CreateUserResponseDict(TypedDict):
    user: UserDict

class UsersGatewayHTTPClient(HTTPClient):
    """
    Клиент взаимодействия с api/v1/users/ сервиса http-gateway
    """
    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по user_id
        :param user_id: идентификатор пользователя
        :return: Ответ от сервера(объект httpx.Respons)
        """

        return self.get(f"/api/v1/users/{user_id}")

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """
        Создание нового пользователя.
        :param request:Словарь данных нового пользователя
        :return: Ответ от сервера (объект httpx.Response)
        """
        return self.post("/api/v1/users", json = request)

    def get_user(self, user_id: str) -> GetUserResponseDict:
        response = self.get_user_api(user_id)
        return response.json()
    def create_user(self) -> CreateUserResponseDict:
        request = CreateUserRequestDict(
            email= fake.email(),
            lastName = fake.last_name(),
            firstName = fake.first_name(),
            middleName= fake.name(),
            phoneNumber= fake.phone_number()
        )
        response = self.create_user_api(request)
        return response.json()


def build_user_gateway_http_client()->UsersGatewayHTTPClient:
    return UsersGatewayHTTPClient(client=build_gateway_http_client())