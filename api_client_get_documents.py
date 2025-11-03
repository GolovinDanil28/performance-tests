from api_client_get_user import create_user_response
from clients.http.gateway.users.client import build_user_gateway_http_client
from clients.http.gateway.cards.client import build_cards_gateway_http_client
from clients.http.gateway.accounts.client import build_account_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client



users_client = build_user_gateway_http_client()
accounts_client = build_account_gateway_http_client()
documents_client = build_documents_gateway_http_client()


create_user_response = users_client.create_user()
print("Create user response:", create_user_response)
user_id = create_user_response.user.id

open_credit_response = accounts_client.open_credit_card_account(user_id)
print("Open credit card account response:", open_credit_response)
account_id = open_credit_response.account.id

tariff_document = documents_client.get_tariff_document(account_id)
print("Get tariff document response:", tariff_document)

contract_document = documents_client.get_contract_document(account_id)
print("Get contract document response:", contract_document)