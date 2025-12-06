from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    """
    Инициализационный хук Locust для выполнения сидинга данных перед запуском теста.
    
    Этот хук выполняется один раз при старте теста и подготавливает тестовые данные:
    1. Создает экземпляр сидинг-сценария ExistingUserGetOperationsSeedsScenario
    2. Выполняет построение тестовых данных методом build()
    3. Загружает данные в окружение Locust методом load()
    
    Args:
        environment (Environment): Окружение Locust, в которое будут загружены данные
        **kwargs: Дополнительные аргументы
    """
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()
    environment.seeds = seeds_scenario.load()


class GetOperationsTaskSet(GatewayGRPCTaskSet):
    """
    TaskSet для имитации поведения существующего пользователя при работе с операциями.
    
    Пользователь последовательно выполняет три типа запросов:
    1. Получение списка своих счетов (реже)
    2. Получение истории операций по счету (чаще)
    3. Получение сводной статистики по операциям (средняя частота)
    
    Attributes:
        seed_user (SeedUserResult): Случайный пользователь, выбранный из сидинговых данных
        selected_account (SeedAccountResult): Выбранный счет пользователя для работы с операциями
    """
    seed_user: SeedUserResult

    def on_start(self) -> None:
        """
        Метод инициализации, выполняющийся перед началом выполнения задач для каждого виртуального пользователя.
        
        Выполняет:
        1. Вызов родительского метода on_start()
        2. Выбор случайного пользователя из сидинговых данных
        3. Проверку наличия счетов у пользователя
        4. Выбор первого доступного счета для работы
        5. Остановку TaskSet, если у пользователя нет счетов
        """
        super().on_start()
        self.seed_user = self.user.environment.seeds.get_next_user()
        
        # В сидинге для этого сценария у пользователя должны быть счета с операциями.
        # Выбираем первый счет для операций (например, первый дебетовый счет).
        # Если дебетовых нет, можно использовать кредитный или другой.
        # Но так как сидинг гарантирует наличие счетов, упрощаем:
        self.selected_account = self.seed_user.debit_card_accounts[0] if self.seed_user.debit_card_accounts else self.seed_user.credit_card_accounts[0]
        print(f"User {self.seed_user.user_id} ready with account {self.selected_account.account_id}")

    @task(3)
    def get_accounts_task(self):
        """
        Задача получения списка счетов пользователя.
        
        Вес задачи: 3 (выполняется реже, чем просмотр операций)
        
        Использует:
        - accounts_gateway_client.get_accounts() для получения всех счетов пользователя
        - user_id из seed_user для идентификации пользователя
        
        Логика:
        Пользователь запрашивает полный список своих счетов для проверки балансов.
        Типичное поведение при входе в приложение или переходе в раздел счетов.
        """
        self.accounts_gateway_client.get_accounts(
            user_id=self.seed_user.user_id
        )

    @task(6)
    def get_operations_task(self):
        """
        Задача получения истории операций по выбранному счету.
        
        Вес задачи: 6 (наиболее часто выполняемая задача)
        
        Использует:
        - operations_gateway_client.get_operations() для получения операций
        - account_id из selected_account для фильтрации операций
        
        Логика:
        Пользователь проверяет историю операций по конкретному счету.
        Типичное поведение после совершения операции или при мониторинге расходов.
        Выполняется чаще других задач, так как пользователь может многократно
        обновлять историю в течение сессии.
        """
        self.operations_gateway_client.get_operations(
            account_id=self.selected_account.account_id
        )

    @task(4)
    def get_operations_summary_task(self):
        """
        Задача получения сводной статистики по операциям.
        
        Вес задачи: 4 (средняя частота выполнения)
        
        Использует:
        - operations_gateway_client.get_operations_summary() для получения статистики
        - account_id из selected_account для фильтрации данных
        
        Логика:
        Пользователь запрашивает агрегированную статистику по операциям
        (суммы по категориям, периодичность операций, график расходов).
        Типичное поведение при анализе расходов или планировании бюджета.
        """
        self.operations_gateway_client.get_operations_summary(
            account_id=self.selected_account.account_id
        )


class GetOperationsScenarioUser(LocustBaseUser):
    """
    Класс виртуального пользователя для сценария получения операций.
    
    Определяет поведение виртуального пользователя в тесте:
    - Использует GetOperationsTaskSet как основной набор задач
    - Наследует базовые настройки ожидания от LocustBaseUser
    
    Параметры пользователя:
    - tasks: Список TaskSet'ов для выполнения (только GetOperationsTaskSet)
    - min_wait: Минимальное время ожидания между задачами (наследуется от родителя)
    - max_wait: Максимальное время ожидание между задачами (наследуется от родителя)
    
    Описание поведения:
    Каждый виртуальный пользователь будет выполнять задачи из GetOperationsTaskSet
    с весами, определенными в методах @task. Время между задачами определяется
    настройками min_wait и max_wait родительского класса.
    """
    tasks = [GetOperationsTaskSet]