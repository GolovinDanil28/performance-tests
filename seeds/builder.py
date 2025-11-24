from clients.grpc.gateway.users.client import UsersGatewayGRPCClient
from clients.grpc.gateway.cards.client import CardsGatewayGRPCClient
from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient
from clients.grpc.gateway.operations.client import OperationsGatewayGRPCClient

from clients.http.gateway.users.client import UsersGatewayHTTPClient
from clients.http.gateway.cards.client import CardsGatewayHTTPClient
from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient
from clients.http.gateway.operations.client import OperationsGatewayHTTPClient
from seeds.schema.plan import SeedsPlan
from seeds.schema.result import SeedAccountResult, SeedsResult, SeedUserResult



class SeedsBuilder:
    def __init__(
            self,
            users_gateway_client: UsersGatewayGRPCClient | UsersGatewayHTTPClient,
            cards_gateway_client: CardsGatewayGRPCClient | CardsGatewayHTTPClient,
            accounts_gateway_client: AccountsGatewayGRPCClient | AccountsGatewayHTTPClient,
            operations_gateway_client: OperationsGatewayGRPCClient | OperationsGatewayHTTPClient
    ):
        self.users_gateway_client = users_gateway_client,
        self.cards_gateway_client = cards_gateway_client,
        self.accounts_gateway_client = accounts_gateway_client,
        self.operations_gateway_client = operations_gateway_client
    
    def build_deposit_account_result(self, user_id: str) -> SeedAccountResult:
        response = self.accounts_gateway_client.open_deposit_account(user_id=user_id)
        return SeedAccountResult(account_id=response.account_id)


    def build_savings_account_result(self, user_id: str) -> SeedAccountResult:
        response = self.accounts_gateway_client.open_saving_account(user_id=user_id)
        return SeedAccountResult(account_id=response.account_id)

    def build_user(self, plan: SeedUserResult) -> SeedUserResult:
        response = self.users_gateway_client.create_user()

        return SeedUserResult(
            user_id=response.user.id,
            deposit_accounts = [
                self.build_deposit_account_result(user_id=response.user_id)
                for _ in range(plan.deposit_accounts.count)
            ],
            savings_accounts = [
                self.build_savings_account_result(user_id=response.user_id) 
                for _ in range(plan.savings_accounts.count)
            ],
            debit_card_accounts = [... for _ in range(plan.debit_card_accounts.count)],
            credit_card_accounts = [... for _ in range(plan.credit_card_accounts.count)]
        )

    def build(self, plan: SeedsPlan) -> SeedsResult:
        return SeedsResult(users=[self.build_user(plan.users) for _ in range(plan.users.count)])
