import time

from clients.http.client import HTTPClient
from httpx import Response, Client
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)

from faker import Faker

fake = Faker()

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

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя.
        :param request:Словарь данных нового пользователя
        :return: Ответ от сервера (объект httpx.Response)
        """
        return self.post("/api/v1/users", json = request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        response = self.get_user_api(user_id)
        #return GetUserResponseSchema(**response.json())
        return GetUserResponseSchema.model_validate_json(response.text)

    def create_user(self) -> CreateUserResponseSchema:
        request = CreateUserRequestSchema(
            email= f"user.{time.time()}@example.com",
            last_name = fake.last_name(),
            first_name = fake.first_name(),
            middle_name= fake.name(),
            phone_number= fake.phone_number()
        )
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_user_gateway_http_client()->UsersGatewayHTTPClient:
    return UsersGatewayHTTPClient(client=build_gateway_http_client())