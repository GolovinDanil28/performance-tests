from locust import User, between, task
from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client
from clients.http.gateway.users.schema import CreateUserResponseSchema


class OpenDebitCardAccountScenarioUser(User):
    host = "localhost"
    wait_time = between(1, 3)
    users_gateway_client: UsersGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    create_user_response: CreateUserResponseSchema

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы инициализируем API-клиенты и создаем нового пользователя.
        """
        # Инициализируем клиент для работы с пользователями
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        
        # Инициализируем клиент для работы со счетами
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)
        
        # Создаем пользователя через API-клиент
        self.create_user_response = self.users_gateway_client.create_user()


    @task
    def open_debit_account(self):
        """
        Основная нагрузочная задача: открытие дебетового счёта для созданного пользователя.
        Используем API-клиент для отправки запроса.
        """
        self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )