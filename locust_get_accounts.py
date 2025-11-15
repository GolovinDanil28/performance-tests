from locust import task, User, between
from clients.http.gateway.locust import GatewayHTTPTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.schema import OpenDepositAccountResponseSchema


class GetAccountsTaskSet(GatewayHTTPTaskSet):
    """
    TaskSet для нагрузочного тестирования операций с пользователями и счетами через HTTP API.
    Задачи выполняются в произвольном порядке.
    """

    create_user_response: CreateUserResponseSchema | None = None
    open_deposit_account_response: OpenDepositAccountResponseSchema | None = None

    @task(2)
    def create_user(self):
        """Задача создания пользователя с весом 2"""
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """Задача открытия депозитного счета с весом 2"""
        # Проверяем, что пользователь уже создан
        if not self.create_user_response:
            return
        
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task(6)
    def get_accounts(self):
        """Задача получения списка счетов с весом 6"""
        # Проверяем, что пользователь уже создан
        if not self.create_user_response:
            return
        
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )


class GetAccountsUser(User):
    """Locust User класс для HTTP сценария получения аккаунта"""
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 3)