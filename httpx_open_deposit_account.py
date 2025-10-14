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
    response_account = httpx.post(f'{base_url}/accounts/open-deposit-account', json=account_data)
    response_account.raise_for_status()

    print(response_account.status_code)
    print(response_account.json())

except httpx.HTTPStatusError as e:
    print(f"Ошибка HTTP: {e.response.status_code} - {e.response.text}")
except KeyError as e:
    print(f"Ошибка в структуре ответа: отсутствует ключ {e}")
except Exception as e:
    print(f"Общая ошибка: {e}")