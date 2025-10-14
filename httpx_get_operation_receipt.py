import httpx
import json
from faker import Faker
fake = Faker()


base_url = 'http://localhost:8003/api/v1'

try:
    user_data = {
        "email": fake.email(),
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "middleName": fake.first_name(),
        "phoneNumber": fake.phone_number()
    }

    response_user = httpx.post(f'{base_url}/users', json=user_data)
    response_user.raise_for_status()

    user_response_data = response_user.json()
    user_id = user_response_data['user']['id']

    account_data = {"userId": user_id}
    response_card_account = httpx.post(f'{base_url}/accounts/open-credit-card-account', json=account_data)
    response_card_account.raise_for_status()
    response_account_data = response_card_account.json()
    response_account_data_id = response_account_data['account']['id']
    response_account_data_cards_id = response_account_data['account']['cards'][0]['id']
    print(response_account_data_id)
    print(response_account_data_cards_id)
    print(response_card_account.status_code)
    print(response_card_account.json())


    make_operation_data = {
            "status": "IN_PROGRESS",
            "amount": 77.99,
            "cardId": response_account_data_cards_id,
            "accountId": response_account_data_id,
            "category": "taxi"
    }

    response_make_purchase_operation = httpx.post(f'{base_url}/operations/make-purchase-operation', json=make_operation_data)
    response_make_purchase_operation_data = response_make_purchase_operation.json()
    print(response_make_purchase_operation_data)
    operation_id = response_make_purchase_operation_data['operation']['id']
    print(operation_id)

    response_get_operation_receipt = httpx.get(f'{base_url}/operations/operation-receipt/{operation_id}')
    print(response_get_operation_receipt.status_code)
    print(response_get_operation_receipt.json())



except httpx.HTTPStatusError as e:
    print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
except KeyError as e:
    print(f"Ошибка в структуре ответа: отсутствует ключ {e}")
except Exception as e:
    print(f"Общая ошибка: {e}")