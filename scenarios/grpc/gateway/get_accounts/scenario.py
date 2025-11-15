from locust import task, User, between
from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import OpenDepositAccountResponse
from contracts.services.users.rpc_create_user_pb2 import CreateUserResponse


class GetAccountsTaskSet(GatewayGRPCTaskSet):
    """
    TaskSet для нагрузочного тестирования операций с пользователями и счетами через gRPC API.
    Задачи выполняются в произвольном порядке.
    """

    create_user_response: CreateUserResponse | None = None
    open_deposit_account_response: OpenDepositAccountResponse | None = None

    @task(2)
    def create_user(self):
        """Задача создания пользователя с весом 2"""
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """Задача открытия депозитного счета с весом 2"""
        if not self.create_user_response:
            return
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task(6)
    def get_accounts(self):
        """Задача получения списка счетов с весом 6"""

        if not self.create_user_response:
            return
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )


class GetAccountsUser(User):
    """Locust User класс для gRPC сценария получения аккаунта"""
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 3)