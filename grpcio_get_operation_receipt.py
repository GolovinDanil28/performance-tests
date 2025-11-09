import grpc
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import OpenDebitCardAccountRequest
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import MakeTopUpOperationRequest
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import GetOperationReceiptRequest
from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from contracts.services.operations.operation_pb2 import OperationStatus
from tools.fakers import fake

# Создаем канал и stub-сервисы
channel = grpc.insecure_channel("localhost:9003")
users_gateway_service = UsersGatewayServiceStub(channel)
accounts_gateway_service = AccountsGatewayServiceStub(channel)
operations_gateway_service = OperationsGatewayServiceStub(channel)

# 1. Создание пользователя
create_user_request = CreateUserRequest(
    email=fake.email(),
    last_name=fake.last_name(),
    first_name=fake.first_name(),
    middle_name=fake.middle_name(),
    phone_number=fake.phone_number()
)
create_user_response = users_gateway_service.CreateUser(create_user_request)
user_id = create_user_response.user.id
print(f"Created user with ID: {user_id}")

# 2. Открытие дебетового счета
open_debit_account_request = OpenDebitCardAccountRequest(user_id=user_id)
open_debit_account_response = accounts_gateway_service.OpenDebitCardAccount(open_debit_account_request)
account_id = open_debit_account_response.account.id
card_id = open_debit_account_response.account.cards[0].id
print(f"Opened account: {account_id} with card: {card_id}")

# 3. Пополнение счета
make_topup_request = MakeTopUpOperationRequest(
    status=OperationStatus.OPERATION_STATUS_COMPLETED,
    amount=fake.amount(),
    card_id=card_id,
    account_id=account_id
)
make_topup_response = operations_gateway_service.MakeTopUpOperation(make_topup_request)
operation_id = make_topup_response.operation.id
print(f"Created top-up operation: {operation_id}")

# 4. Получение чека по операции
get_receipt_request = GetOperationReceiptRequest(operation_id=operation_id)
get_receipt_response = operations_gateway_service.GetOperationReceipt(get_receipt_request)

# 5. Логирование результата
print("Get operation receipt response: receipt {")
print(f'  url: "{get_receipt_response.receipt.url}"')
print(f'  document: "{get_receipt_response.receipt.document}"')
print("}")