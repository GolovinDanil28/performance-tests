from locust import HttpUser, between, task
from tools.fakers import fake


class OpenDebitCardAccountScenarioUser(HttpUser):
    wait_time = between(1, 3)
    user_id: str

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        user_data = {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }

        with self.client.post(
            "/api/v1/users", 
            json=user_data,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                self.user_id = response.json()["user"]["id"]
            else:
                response.failure(f"User creation failed: {response.status_code}")

    @task
    def open_debit_account(self):
        """
        Основная нагрузочная задача: открытие дебетового счёта для созданного пользователя.
        Здесь мы выполняем POST-запрос к /api/v1/accounts/open-debit-card-account,
        передавая ранее полученный user_id в теле запроса.
        """
        account_data = {
            "user_id": self.user_id
        }
        
        self.client.post(
            "/api/v1/accounts/open-debit-card-account",
            json=account_data
        )