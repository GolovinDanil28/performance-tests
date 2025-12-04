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
    
    Args:
        environment (Environment): Окружение Locust, в которое будут загружены данные
        **kwargs: Дополнительные аргументы
    """
    # Создаем экземпляр сидинг-сценария
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()

    # Выполняем генерацию данных, если они ещё не созданы
    seeds_scenario.build()

    # Загружаем сгенерированных пользователей в окружение Locust
    environment.seeds = seeds_scenario.load()


class IssueVirtualCardTaskSet(GatewayHTTPTaskSet):
    """
    TaskSet для имитации поведения существующего пользователя при выпуске виртуальной карты.
    
    Пользователь выполняет два основных действия:
    1. Получение списка своих счетов (частое действие)
    2. Выпуск новой виртуальной карты (редкое действие)
    
    Особенности поведения:
    - Пользователь редко выпускает карты (weight=1)
    - Часто проверяет счета (weight=4)
    - После выпуска карты пользователь ожидает увидеть её в списке карт, привязанных к счёту
    
    Attributes:
        seed_user (SeedUserResult): Случайный пользователь, выбранный из сидинговых данных
        selected_account (SeedAccountResult): Выбранный дебетовый счет для выпуска карты
    """
    
    seed_user: SeedUserResult

    def on_start(self) -> None:
        """
        Метод инициализации, выполняющийся перед началом выполнения задач для каждого виртуального пользователя.
        
        Выполняет:
        1. Вызов родительского метода on_start()
        2. Выбор случайного пользователя из сидинговых данных
        3. Проверку наличия дебетовых счетов у пользователя
        4. Выбор первого дебетового счета для выпуска виртуальной карты
        5. Остановку TaskSet, если у пользователя нет дебетовых счетов
        """
        super().on_start()

        # Получаем случайного пользователя из списка
        self.seed_user = self.user.environment.seeds.get_random_user()
        
        # Проверяем, что у пользователя есть дебетовые счета
        if not self.seed_user.debit_card_accounts:
            print(f"User {self.seed_user.user_id} has no debit card accounts")
            self.stop(True)
        else:
            # Выбираем первый дебетовый счет для выпуска карты
            self.selected_account = self.seed_user.debit_card_accounts[0]
            print(f"User {self.seed_user.user_id} ready with account {self.selected_account.account_id}")

    @task(4)
    def get_accounts(self):
        """
        Задача получения списка счетов пользователя.
        
        Вес задачи: 4 (частое действие)
        
        Логика:
        - Пользователь запрашивает список своих счетов для проверки баланса
        - Это базовая операция, с которой обычно начинается взаимодействие с приложением
        - После выпуска карты пользователь повторно запрашивает список счетов, 
          чтобы убедиться, что карта появилась в составе счета
        
        Использует:
        - accounts_gateway_client.get_accounts() для получения всех счетов пользователя
        - user_id из seed_user для идентификации пользователя
        """
        # Запрашиваем список счетов
        self.accounts_gateway_client.get_accounts(
            user_id=self.seed_user.user_id
        )

    @task(1)
    def issue_virtual_card(self):
        """
        Задача выпуска новой виртуальной карты.
        
        Вес задачи: 1 (редкое действие)
        
        Логика:
        - Пользователь выпускает виртуальную карту для онлайн-покупок или разовых операций
        - Это редкая операция, которая выполняется один раз, а не массово
        - Виртуальная карта привязывается к дебетовому счету пользователя
        - Отражает реальное поведение: пользователь не выпускает 10-20 карт подряд
        
        Использует:
        - cards_gateway_client.issue_virtual_card() для создания виртуальной карты
        - user_id из seed_user для идентификации пользователя
        - account_id из selected_account для привязки карты к счету
        """
        # Выпускаем виртуальную карту для дебетового счета
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.selected_account.account_id
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """
    Класс виртуального пользователя для сценария выпуска виртуальной карты.
    
    Определяет поведение виртуального пользователя в тесте:
    - Использует IssueVirtualCardTaskSet как основной набор задач
    - Наследует базовые настройки ожидания от LocustBaseUser
    
    Параметры пользователя:
    - tasks: Список TaskSet'ов для выполнения (только IssueVirtualCardTaskSet)
    - min_wait: Минимальное время ожидания между задачами (наследуется от родителя)
    - max_wait: Максимальное время ожидание между задачами (наследуется от родителя)
    
    Описание поведения:
    Каждый виртуальный пользователь будет выполнять задачи из IssueVirtualCardTaskSet
    с весами, определенными в методах @task. Время между задачами определяется
    настройками min_wait и max_wait родительского класса.
    
    Модель нагрузки:
    - 8 пользователей создаются со скоростью 1 пользователь/сек
    - Длительность теста: 4 минуты
    - Соотношение запросов: 4 запроса счетов на 1 запрос выпуска карты
    """
    
    tasks = [IssueVirtualCardTaskSet]