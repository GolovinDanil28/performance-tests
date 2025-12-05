from locust import task
from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountResponse
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import IssuePhysicalCardResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    """
    Последовательный TaskSet для сценария выпуска физической карты новым пользователем.
    Задачи выполняются строго последовательно в порядке объявления.
    """

    create_user_response: CreateUserResponse | None = None
    open_debit_account_response: OpenDebitCardAccountResponse | None = None
    issue_physical_card_response: IssuePhysicalCardResponse | None = None

    @task
    def create_new_user(self):
        """Шаг 1: Создание нового пользователя"""
        self.create_user_response = self.users_gateway_client.create_user()
    
    @task  
    def open_debit_card_account(self):
        """Шаг 2: Открытие дебетового счета для пользователя"""
        if not self.create_user_response:
            return
            
        self.open_debit_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )
    
    @task
    def get_accounts_to_verify(self):
        """Шаг 3: Получение информации о счетах для проверки"""
        if not self.create_user_response:
            return
            
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )
    
    @task
    def issue_physical_card_to_account(self):
        """Шаг 4: Выпуск физической карты для дебетового счета"""
        if not self.create_user_response:
            return
            
        if not self.open_debit_account_response or not self.open_debit_account_response.account:
            return
            
        if hasattr(self, 'cards_gateway_client'):
            self.issue_physical_card_response = self.cards_gateway_client.issue_physical_card(
                user_id=self.create_user_response.user.id,
                account_id=self.open_debit_account_response.account.id
            )


class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """Locust User класс для сценария выпуска физической карты"""
    tasks = [IssuePhysicalCardSequentialTaskSet]