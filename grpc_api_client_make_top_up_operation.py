from clients.grpc.gateway.users.client import build_users_gateway_grpc_client
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client


def main():
    # Инициализация клиентов
    users_client = build_users_gateway_grpc_client()
    accounts_client = build_accounts_gateway_grpc_client()
    operations_client = build_operations_gateway_grpc_client()

    # 1. Создание пользователя
    create_user_response = users_client.create_user()
    print("Create user response:", create_user_response)
    user_id = create_user_response.user.id

    # 2. Открытие дебетового счета
    open_debit_account_response = accounts_client.open_debit_card_account(user_id)
    print("Open debit card account response:", open_debit_account_response)
    account_id = open_debit_account_response.account.id
    
    # Получаем ID первой карты из счета
    card_id = open_debit_account_response.account.cards[0].id

    # 3. Создание операции пополнения
    make_top_up_response = operations_client.make_top_up_operation(card_id, account_id)
    print("Make top up operation response:", make_top_up_response)


if __name__ == "__main__":
    main()