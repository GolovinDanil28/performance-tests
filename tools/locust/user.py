from locust import User, between


class LocustBaseUser(User):
    """
    Пользователь Locust, исполняющий последовательный сценарий получения документов.
    """
    host = "localhost"
    abstract = True
    wait_time = between(1, 3)