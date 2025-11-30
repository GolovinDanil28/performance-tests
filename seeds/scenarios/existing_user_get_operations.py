from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan, SeedCardsPlan, SeedOperationsPlan


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который просматривает операции по кредитному счёту.
    Создаём 300 пользователей, каждому из которых открывается один кредитный счёт
    с операциями: 5 покупок, 1 пополнение, 1 снятие наличных.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        Возвращает план сидинга для создания пользователей и их кредитных счетов с операциями.
        Мы создаём 300 пользователей, каждый получит один кредитный счёт с операциями.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Создаём 300 пользователей
                credit_card_accounts=SeedAccountsPlan(
                    count=1,  # Один кредитный счёт на пользователя
                    purchase_operations=SeedOperationsPlan(count=5),  # 5 операций покупки
                    top_up_operations=SeedOperationsPlan(count=1),    # 1 операция пополнения
                    cash_withdrawal_operations=SeedOperationsPlan(count=1),  # 1 операция снятия наличных
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Возвращает название сценария сидинга.
        Это имя будет использоваться для сохранения данных сидинга.
        """
        return "existing_user_get_operations"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.
    """
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # Запуск сидинга
    seeds_scenario.load()   # Загрузка и вывод результатов