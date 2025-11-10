from clients.grpc.gateway.users.client import build_users_gateway_grpc_client
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.documents.client import build_documents_gateway_grpc_client


def main():
    # Инициализация клиентов
    users_client = build_users_gateway_grpc_client()
    accounts_client = build_accounts_gateway_grpc_client()
    documents_client = build_documents_gateway_grpc_client()

    # 1. Создание пользователя
    create_user_response = users_client.create_user()
    print("Create user response:", create_user_response)
    user_id = create_user_response.user.id

    # 2. Открытие кредитного счета
    open_credit_response = accounts_client.open_credit_card_account(user_id)
    print("Open credit card account response:", open_credit_response)
    account_id = open_credit_response.account.id

    # 3. Получение документа тарифа
    tariff_document = documents_client.get_tariff_document(account_id)
    print("Get tariff document response:", tariff_document)

    # 4. Получение документа контракта
    contract_document = documents_client.get_contract_document(account_id)
    print("Get contract document response:", contract_document)


if __name__ == "__main__":
    main()