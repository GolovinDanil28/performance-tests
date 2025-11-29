# Импортируем gRPC-билдер
from seeds.builder import build_grpc_seeds_builder

# Импортируем функции для сохранения и загрузки данных
from seeds.dumps import save_seeds_result, load_seeds_result

# Импортируем схемы плана сидинга (описывают структуру данных)
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedCardsPlan, SeedAccountsPlan, SeedOperationsPlan  # Добавлен SeedOperationsPlan
import time



builder = build_grpc_seeds_builder()

result = builder.build(
    SeedsPlan(
        users=SeedUsersPlan(
            count=100,
            savings_accounts=SeedAccountsPlan(count=0),
            deposit_accounts=SeedAccountsPlan(count=0),
            debit_card_accounts=SeedAccountsPlan(
                count=1,
                physical_cards=SeedCardsPlan(count=1),
                virtual_cards=SeedCardsPlan(count=2),
                top_up_operations=SeedOperationsPlan(count=3),
                purchase_operations=SeedOperationsPlan(count=2),
                transfer_operations=SeedOperationsPlan(count=1),
                cash_withdrawal_operations=SeedOperationsPlan(count=1)
            ),
            credit_card_accounts=SeedAccountsPlan(
                count=1,
                physical_cards=SeedCardsPlan(count=1),
                virtual_cards=SeedCardsPlan(count=1),
                top_up_operations=SeedOperationsPlan(count=2),
                purchase_operations=SeedOperationsPlan(count=3),
                transfer_operations=SeedOperationsPlan(count=1),
                cash_withdrawal_operations=SeedOperationsPlan(count=2)
            )
        )
    )
)


# Шаг 3. Сохраняем результат сидинга в файл, привязанный к сценарию "test-scenario"
save_seeds_result(result=result, scenario=f"test-scenario+{time.time()}")

# Шаг 4. Загружаем данные из файла и выводим в консоль
print(load_seeds_result(scenario="test-scenario"))