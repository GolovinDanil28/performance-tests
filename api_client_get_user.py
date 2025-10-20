import time
from clients.http.gateway.users.client import build_user_gateway_http_client

from faker import Faker

fake = Faker()

users_gateway_client = build_user_gateway_http_client()
create_user_response = users_gateway_client.create_user()
print('Create user data:' , create_user_response)

get_user_response = users_gateway_client.get_user(create_user_response['user']['id'])

print('Get user data:' , get_user_response)