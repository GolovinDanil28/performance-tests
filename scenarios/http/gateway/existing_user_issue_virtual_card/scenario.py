from locust import task, events
from locust.env import Environment

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    """
    Инициализационный хук Locust для выполнения сидинга данных перед запуском теста.
    
    Этот хук выполняется один раз при старте теста и подготавливает тестовые данные:
    1. Создает экземпляр сидинг-сценария ExistingUserIssueVirtualCardSeedsScenario
    2. Выполняет построение тестовых данных методом build()
    3. Загружает данные в окружение Locust методом load()
    """
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()
    environment.seeds = seeds_scenario.load()


class IssueVirtualCardTaskSet(GatewayHTTPTaskSet):
    """
    TaskSet для имитации поведения существующего пользователя при выпуске виртуальной карты.
    
    Пользователь выполняет два основных действия:
    1. Получение списка счетов (частое действие)
    2. Выпуск новой виртуальной карты (редкое действие)
    
    Особенности поведения:
    - Пользователь редко выпускает карты (weight=1)
    - Часто проверяет счета (weight=4)
    - После выпуска карты пользователь ожидает увидеть её в списке карт, привязанных к счёту
    """
    
    seed_user: SeedUserResult

    def on_start(self) -> None:
        """
        Метод инициализации, выполняющийся перед началом выполнения задач для каждого виртуального пользователя.
        
        Выполняет:
        1. Вызов родительского метода on_start()
        2. Получение следующего пользователя из сидинговых данных (последовательно)
        3. Установка выбранного счета (первый дебетовый счет пользователя)
        """
        super().on_start()
        self.seed_user = self.user.environment.seeds.get_next_user()
    
        self.selected_account = self.seed_user.debit_card_accounts[0]

    @task(4)
    def get_accounts(self):
        """
        Задача получения списка счетов пользователя.
        
        Вес задачи: 4 (частое действие)
        """
        self.accounts_gateway_client.get_accounts(
            user_id=self.seed_user.user_id
        )

    @task(1)
    def issue_virtual_card(self):
        """
        Задача выпуска новой виртуальной карты.
        
        Вес задачи: 1 (редкое действие)
        """
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.selected_account.account_id
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """
    Класс виртуального пользователя для сценария выпуска виртуальной карты.
    """
    tasks = [IssueVirtualCardTaskSet]