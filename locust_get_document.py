from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from locust import User,between,task
from clients.http.gateway.users.schema import CreateUserResponseSchema
from clients.http.gateway.accounts.schema import OpenSavingsAccountResponseSchema


class GetDocumentsSequentialTaskSet(GatewayHTTPSequentialTaskSet):

    create_user_response: CreateUserResponseSchema | None = None
    open_savings_account_response: OpenSavingsAccountResponseSchema | None = None

    @task
    def create_user(self):
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_saving_account(self):
        if not self.create_user_response:
            return



        self.open_savings_account_response = self.accounts_gateway_client.open_savings_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def get_document(self):
        if not self.open_savings_account_response:
            return
        
        self.documents_gateway_client.get_tariff_document(
            account_id=self.open_savings_account_response.account.id
        )
        self.documents_gateway_client.get_contract_document(
            account_id=self.open_savings_account_response.account.id
        )

class GetDocumentsUser(User):
    host = "localhost"
    tasks = [GetDocumentsSequentialTaskSet]
    wait_time = between(1, 3)