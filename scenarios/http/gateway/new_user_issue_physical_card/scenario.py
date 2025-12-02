from locust import task
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.cards.schema import IssuePhysicalCardResponseSchema
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """
    Последовательный TaskSet для сценария выпуска физической карты новым пользователем.
    Задачи выполняются строго последовательно в порядке объявления.
    """

    create_user_response: CreateUserResponseSchema | None = None
    open_debit_account_response: OpenDebitCardAccountResponseSchema | None = None
    issue_physical_card_response: IssuePhysicalCardResponseSchema | None = None

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