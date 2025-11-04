import grpc
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest
from tools.fakers import fake


def main():
    # Создаем канал связи с сервером
    channel = grpc.insecure_channel("localhost:9003")

    # Инициализируем клиентов сервисов
    users_client = UsersGatewayServiceStub(channel)
    accounts_client = AccountsGatewayServiceStub(channel)

    # Генерируем тестовые данные пользователя
    user_data = {
        "email": fake.email(),
        "last_name": fake.last_name(),
        "first_name": fake.first_name(),
        "middle_name": fake.middle_name(),
        "phone_number": fake.phone_number()
    }

    # Создаем пользователя
    create_user_request = CreateUserRequest(**user_data)
    create_user_response = users_client.CreateUser(create_user_request)

    print("Create user response:", create_user_response)

    # Открываем дебетовый счет для созданного пользователя
    open_account_request = OpenDebitCardAccountRequest(
        user_id=create_user_response.user.id
    )
    open_account_response = accounts_client.OpenDebitCardAccount(open_account_request)

    print("\nOpen debit card account response:", open_account_response)


if __name__ == "__main__":
    main()