from clients.http.gateway.users.client import build_user_gateway_http_client
from clients.http.gateway.accounts.client import build_account_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client

users_client = build_user_gateway_http_client()
accounts_client = build_account_gateway_http_client()
operations_client = build_operations_gateway_http_client()

create_user_response = users_client.create_user()
print("Create user response:", create_user_response)
user_id = create_user_response.user.id

open_debit_account_response = accounts_client.open_debit_card_account(user_id)
print("Open debit card account response:", open_debit_account_response)
account_id = open_debit_account_response.account.id

card_id = open_debit_account_response.account.cards[0].id

make_top_up_response = operations_client.make_top_up_operation(card_id, account_id)
print("Make top up operation response:", make_top_up_response)