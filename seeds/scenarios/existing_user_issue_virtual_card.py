from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedCardsPlan, SeedOperationsPlan


class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который выпускает виртуальную карту для своего дебетового счёта.
    Создаём 300 пользователей, каждому из которых открывается один дебетовый счёт.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        Возвращает план сидинга для создания пользователей и их дебетовых счетов.
        Мы создаём 300 пользователей, каждый получит один дебетовый счёт.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Создаём 300 пользователей
                debit_card_accounts=SeedAccountsPlan(count=1),
                # Остальные типы счетов не создаём
                savings_accounts=SeedAccountsPlan(count=0),
                deposit_accounts=SeedAccountsPlan(count=0),
                credit_card_accounts=SeedAccountsPlan(count=0)
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Возвращает название сценария сидинга.
        Это имя будет использоваться для сохранения данных сидинга.
        """
        return "existing_user_issue_virtual_card"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.
    """
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()  # Запуск сидинга
    seeds_scenario.load()   # Загрузка и вывод результатов