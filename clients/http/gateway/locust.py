from locust import TaskSet, SequentialTaskSet
from clients.http.gateway.users.client import (build_users_gateway_locust_http_client,
    UsersGatewayHTTPClient)
from clients.http.gateway.cards.client import (build_cards_gateway_locust_http_client,
    CardsGatewayHTTPClient)
from clients.http.gateway.accounts.client import (AccountsGatewayHTTPClient,
    build_accounts_gateway_locust_http_client)
from clients.http.gateway.documents.client import (build_documents_gateway_locust_http_client,
    DocumentsGatewayHTTPClient)
from clients.http.gateway.operations.client import (build_operations_gateway_locust_http_client,
    OperationsGatewayHTTPClient)



class GatewayHTTPTaskSet(TaskSet):
    users_gateway_client: UsersGatewayHTTPClient
    cards_gateway_client: CardsGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    documents_gateway_client: DocumentsGatewayHTTPClient
    operations_gateway_client: OperationsGatewayHTTPClient
    def on_start(self) -> None:
        self.users_gateway_client = build_users_gateway_locust_http_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_http_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_http_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_http_client(self.user.environment)



class GatewayHTTPSequentialTaskSet(SequentialTaskSet):
    users_gateway_client: UsersGatewayHTTPClient
    cards_gateway_client: CardsGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    documents_gateway_client: DocumentsGatewayHTTPClient
    operations_gateway_client: OperationsGatewayHTTPClient
    def on_start(self) -> None:
        self.users_gateway_client = build_users_gateway_locust_http_client(self.user.environment)
        self.cards_gateway_client = build_cards_gateway_locust_http_client(self.user.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.user.environment)
        self.documents_gateway_client = build_documents_gateway_locust_http_client(self.user.environment)
        self.operations_gateway_client = build_operations_gateway_locust_http_client(self.user.environment)