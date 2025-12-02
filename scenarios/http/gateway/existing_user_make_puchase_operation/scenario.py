from locust import task, events
from locust.env import Environment

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_make_purchase_operation import ExistingUserMakePurchaseOperationSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser

@events.init.add_listener
def init(environment: Environment, **kwargs):
    seeds_scenario = ExistingUserMakePurchaseOperationSeedsScenario()
    seeds_scenario.build()
    environment.seeds = seeds_scenario.load()

class ExistingMakePurchaseOperationTaskSet(GatewayHTTPTaskSet):
    seed_user: SeedUserResult

    def on_start(self) -> None:
        super().on_start()
        self.seed_user = self.user.environment.seeds.get_random_user()
        if not self.seed_user.credit_card_accounts:
            print(f"User {self.seed_user.user_id} has no credit card accounts")
            self.stop(True)
        elif not self.seed_user.credit_card_accounts[0].physical_cards:
            print(f"User {self.seed_user.user_id} has no physical cards")
            self.stop(True)
        else:
            print(f"User {self.seed_user.user_id} ready with card {self.seed_user.credit_card_accounts[0].physical_cards[0].card_id}")
    
    @task(1)
    def make_purchase_operation_task(self):
        try:
            self.operations_gateway_client.make_purchase_operation(
                card_id=self.seed_user.credit_card_accounts[0].physical_cards[0].card_id,
                account_id=self.seed_user.credit_card_accounts[0].account_id
            )
        except Exception as e:
            print(f"Purchase operation failed: {e}")
    
    @task(2)
    def get_accounts(self):
        self.accounts_gateway_client.get_accounts(
            user_id=self.seed_user.user_id
        )

    @task(2)
    def get_operations(self):
        self.operations_gateway_client.get_operations(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )
    
    @task(2)
    def get_operation_summary(self):
        self.operations_gateway_client.get_operations_summary(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

class ExistingUserMakePurchaseOperationScenarioUser(LocustBaseUser):
    tasks = [ExistingMakePurchaseOperationTaskSet]