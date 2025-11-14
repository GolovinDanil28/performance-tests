from locust import HttpUser, between, task
from tools.fakers import fake


class GetUserScenarioUser(HttpUser):
    wait_time = between(1, 3)
    user_data: dict


    def on_start(self) -> None:
        request =  {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }

        response = self.client.post("/api/v1/users", json= request)
        self.user_data = response.json()

    @task
    def get_user(self):
        
        self.client.get(
            f"/api/v1/users/{self.user_data['user']['id']}",
            name="/api/v1/users/{user_id}"
        )


